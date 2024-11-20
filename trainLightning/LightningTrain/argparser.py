import argparse

def get_args():
    parser = argparse.ArgumentParser(description="argument parser for PyTorch Lightning project")
    
    parser.add_argument('--batch_size', type=int, default=32, help='input batch size for training (default: 32)')
    parser.add_argument('--epochs', type=int, default=10, help='number of epochs to train (default: 10)')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='learning rate (default: 0.001)')
    parser.add_argument('--data_train_path', type=str, help='path to the dataset used for training')
    parser.add_argument('--data_test_path', type=str, help='path to the dataset used for testing')
    parser.add_argument('--model_path', type=str, default='./models', help='path to save the trained model (default: ./models)')
    parser.add_argument('--train_data', type=bool, default='True', help='train or test the model (default: True)')
    
    args = parser.parse_args()
    return args