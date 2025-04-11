from setuptools import setup

setup(
    name="deepfake_generator",
    version="1.0.0",
    packages=[""],
    install_requires=[
        "opencv-python",
        "numpy",
        "mediapipe",
        "tqdm"
    ],
    entry_points={
        'console_scripts': [
            'deepfake-cli=cli_app:main',
        ],
        'gui_scripts': [
            'deepfake-gui=desktop_app:main',
        ],
    }
)
