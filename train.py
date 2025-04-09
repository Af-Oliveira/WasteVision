import torch
import os
import argparse
import importlib.util

def import_model_train_script(model_name):
    # Construct the path to the model-specific train.py
    model_folder = os.path.join("models", model_name)
    train_script_path = os.path.join(model_folder, "train.py")

    if os.path.exists(train_script_path):
        # Load the model-specific train.py dynamically
        spec = importlib.util.spec_from_file_location("train_script", train_script_path)
        train_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(train_module)
        return train_module
    else:
        print(f"[ERROR] Model {model_name} not found in models folder.")
        return None

def main():
    parser = argparse.ArgumentParser(description="Centralized AI Training Script")

    parser.add_argument("--type", required=True, choices=["classification", "single-stage", "two-stage"],
                        help="Type of task: classification | single-stage | two-stage")
    parser.add_argument("--model", required=True,
                        help="Model to train, e.g., yolo, vit, fast-rcc, ssd")
    parser.add_argument("--data", default="dataset/data.yaml", help="Path to dataset or config YAML")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch_size", type=int, default=32)

    args = parser.parse_args()
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    print(f"[INFO] Using device: {device}")
    print(f"[INFO] Training {args.model} for {args.type} task")

    # Dynamically load the model's training script
    model_train_module = import_model_train_script(args.model)


    if model_train_module:
        if args.type == "single-stage":
            if hasattr(model_train_module, "train_single_stage"):
                model_train_module.train_single_stage(args.model, args.data, args.epochs, args.batch_size, device)
            else:
                print(f"[ERROR] {args.model} does not have a 'train_single_stage' function.")
        elif args.type == "two-stage":
            if hasattr(model_train_module, "train_two_stage"):
                model_train_module.train_two_stage(args.data, args.epochs, args.batch_size, device)
            else:
                print(f"[ERROR] {args.model} does not have a 'train_two_stage' function.")
        elif args.type == "classification":
            if hasattr(model_train_module, "train_classification"):
                model_train_module.train_classification(args.data, args.epochs, args.batch_size, device)
            else:
                print(f"[ERROR] {args.model} does not have a 'train_classification' function.")
        else:
            print("[ERROR] Invalid training type.")
    else:
        print("[ERROR] Model training script could not be loaded.")

if __name__ == "__main__":
    main()