import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import copy

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        return x
    
    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if (not os.path.exists(model_folder_path)):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        print("learning rate: ")
        print(self.lr)
        self.gamma = gamma
        self.model = model
        if model.linear1.weight is not None:
            print("Initial weights for Linear1:")
            print(self.model.linear1.weight)
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with the current state
        pred = self.model(state)
        if torch.allclose(pred, torch.tensor([[0.]])):
            print('Predicted Q-values:', pred)
        if self.model.linear1.weight.grad is not None:
            print("Gradients for Linear1 weights:")
            print(self.model.linear1.weight.grad)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new

        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()

if __name__ == "__main__":
    LR = .00025
    g = 0.85
    model = Linear_QNet(5, 256, 1)
    trainer = QTrainer(model, lr=LR, gamma=g)

    # Assuming 'model' is your PyTorch model
    # You can create a deep copy of the model to compare gradients
    model_copy = copy.deepcopy(model)

    # Define a small dummy input tensor
    dummy_input = torch.randn(1, input_size)  # Adjust 'input_size' to match your model's input size

    # Forward pass
    output = model(dummy_input)
    loss = your_loss_function(output, target)  # Define your loss function and target

    # Backward pass
    loss.backward()

    # Compare gradients before and after backpropagation
    for name, param in model.named_parameters():
        if param.grad is not None:
            # Get the corresponding parameter from the copied model
            param_copy = getattr(model_copy, name)

            # Calculate the gradient scaling factor
            gradient_scaling_factor = param.grad.norm() / param_copy.grad.norm()

            # Print the name of the parameter and the scaling factor
            print(f"Parameter: {name}, Gradient Scaling Factor: {gradient_scaling_factor}")

    # Reset gradients
    model.zero_grad()
    model_copy.zero_grad()