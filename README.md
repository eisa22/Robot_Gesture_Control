# Robot Control via Hand Gestures

This project demonstrates controlling an e.DO robot using hand gestures detected via Mediapipe. The system captures hand gestures through a camera, processes them to recognize specific gestures, and then translates these gestures into commands to control the e.DO robot.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

The goal of this project is to create an intuitive way to control the e.DO robot using simple hand gestures. By leveraging Mediapipe's hand tracking capabilities, we can detect and interpret various hand gestures, which are then mapped to specific commands for the e.DO robot. This makes it possible to perform various robotic tasks in a more natural and interactive manner.

## Features

- **Hand Gesture Recognition:** Utilizes Mediapipe to track and recognize hand gestures.
- **e.DO Robot Control:** Sends commands to the e.DO robot based on the recognized gestures.
- **Real-time Processing:** Processes hand gestures and controls the robot in real-time.
- **Easy Setup:** Simple installation and setup using `environment.yml`.

## Installation

To get started, clone this repository and install the necessary dependencies. We recommend using conda to manage the environment.

1. Clone the repository:
   ```sh
   git clone https://github.com/eisa22/Robot_Gesture_Control.git
   ```

2. Create and activate the conda environment:
   ```sh
   conda env create -f environment.yml
   conda activate robot-control-env
   ```

This will install all the required libraries and dependencies specified in the `environment.yml` file.

## Usage

To run the program, simply execute the main script. Ensure that your camera is properly set up and connected, and that the e.DO robot is powered on and ready to receive commands.

1. Start the program:
   ```sh
   python main.py
   ```

2. Follow the on-screen instructions to perform gestures and control the robot.

## Contributing

We welcome contributions to this project. If you have an idea for improvement or have found a bug, please open an issue or submit a pull request. 

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

This project uses the following open-source libraries and tools:

- [Mediapipe](https://mediapipe.dev/) - For hand gesture recognition.
- [eDO Robot](https://www.comau.com/en/edo/) - The robot used for demonstrating gesture control.

Special thanks to all the contributors and the open-source community for their valuable resources and support.
