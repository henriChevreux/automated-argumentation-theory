On a clean Python 3 virtual environment (strongly recommended):
1. Run ‘pip3 install -r requirements.py’
2. Run ‘python3 CLI_predict_relationships.py run-pipeline FILEPATH’, with FIELPATH the path to a csv file. Make sure the first two rows of the csv file contain the pairs of arguments. An example file is provided in ‘in/ACMToIT2017_dataset.csv’, making the command using this file: ‘python3 CLI_predict_relationships.py run-pipeline in/ACMToIT2017_dataset.csv’

After running the pipeline, the output folder should contain:
- A timestamped csv file containing the relationships between pairs of arguments
- A timestamped af file containing the abstract argumentation framework
- A timestamped pkl file containing the arguments dictionary