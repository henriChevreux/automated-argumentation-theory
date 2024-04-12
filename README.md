# Argument Analysis Pipeline

The Discourse Analysis Pipeline is a sophisticated software tool designed to automate the analysis of argumentative structures in textual content, utilising principles from Argumentation Theory and leveraging advancements in Artificial Intelligence (AI) and Natural Language Processing (NLP) to perform reasoning tasks on a set of arguments.

## Getting Started

These instructions will guide you on how to set up and run the Argument Analysis Pipeline on your local machine for development and testing purposes.

### Prerequisites

Before running the pipeline, ensure you have the following software installed on your system:

- Python 3.9
- pip (Python package installer)
- Git (for version control)
- Git Large File Storage (LFS) for managing large files

### Installing Git Large File Storage (LFS)

Git LFS is essential in this project for downloading the pre-trained model files in this project. Follow these steps to install Git LFS:

1. **Download and Install Git LFS:**
   Visit [Git LFS](https://git-lfs.github.com) and download the version compatible with your operating system. Follow the installation instructions provided on the website.

2. **Initialize Git LFS:**
   Once Git LFS is installed, run the following command in your terminal to set up Git LFS for your user account:`git lfs install`

## Installing the Pipeline
1. **Clone the Repository:**
Start by cloning this repository to your local machine using Git LFS:

```
git lfs clone https://github.com/henriChevreux automated-argumentation-theory.git
```


2. **Set Up a Virtual Environment (Optional):**
It is highly recommended to set up a Python virtual environment for running the pipeline:
```
python -m venv venv
source venv/bin/activate
# On Windows, use `venv\Scripts\activate`
```

3. **Install Required Packages:**
Install all the required Python packages using the command:
```
pip install -r requirements.txt
```
You're ready to go!
 


## Running the Pipeline

To execute the pipeline with specific input files and model configurations, use the following command structure:


### Example Command

For example, to run the pipeline with the input file located at `in/arguments_test.txt` and using the `advanced` model, you would use:

`python3 CLI_pipeline.py run-pipeline in/arguments_test.txt --model advanced`

This command initiates the pipeline, processing the specified input file with the chosen model. Ensure that your path to the input file and the model name are correctly specified as per your project setup.

### Details

- **[input file path]**: Replace this with the path to your input text file that contains the list of arguments, separated by a full stop. Example files are included in the `in` folder.
- **[model type]**: Replace this with the model configuration you wish to use. Currently, two pre-trained models are available:
  -  `simple`: This model is a lightweight version of the model, which aims to balance accuracy with computational complexity, for testing purposes. This is the model used by default.
  -  `advanced`: This model is the more accurate, more complex model. You can use this model by adding the argument `--model advanced` to your command.

Follow the on-screen prompts to progress through the pipeline's execution phases. The pipeline will output its analysis to the output directory.

## Output

The pipeline will generate several outputs based on the analysis performed, including the relationships between arguments and a constructed abstract argumentation framework. These outputs are all saved in the `out/` directory. Make sure to check this directory after the run to view your results.

After running the pipeline, the output folder should contain:
- A timestamped `csv` file containing the contructed pairs of arguments.
- A timestamped `csv` file containing the relationships between pairs of arguments.
- A timestamped `af` file containing the abstract argumentation framework.
- A timestamped `pkl` file containing the arguments dictionary.


Enjoy :)