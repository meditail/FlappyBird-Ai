# FlappyBird-AI

FlappyBird-AI is a Python-based recreation of the popular game Flappy Bird. It also includes an Artificial Intelligence (AI) that learns to play the game using Q-Learning.

## Installation

To get started, make sure you have Python installed on your system. Then, install all the required dependencies by running the following command:

```
pip install -r requirements.txt
```

## Training

The AI model can be trained by providing two parameters. The first parameter specifies the mode, which can be either "train" or "test". The second parameter determines the number of training episodes to run. A recommended value for training episodes is 500,000. You can start the training process with the following command:
```
python main.py train 500000
```

During training, the program will display the mean score of the last 100 training episodes as the output, which indicates the progress of the learning process.

## Testing

To evaluate the performance of the trained AI model, you can run the following command:

```
python main.py test
```

This will start the Flappy Bird game with the trained AI model, allowing you to observe its performance.
