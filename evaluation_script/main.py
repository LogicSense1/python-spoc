import random


def evaluate(test_annotation_file, user_submission_file, phase_codename, **kwargs):
    print("Starting Evaluation.....")
    """
    Evaluates the submission for a particular challenge phase and returns score
    Arguments:

        `test_annotations_file`: Path to test_annotation_file on the server
        `user_submission_file`: Path to file submitted by the user
        `phase_codename`: Phase to which submission is made

        `**kwargs`: keyword arguments that contains additional submission
        metadata that challenge hosts can use to send slack notification.
        You can access the submission metadata
        with kwargs['submission_metadata']

        Example: A sample submission metadata can be accessed like this:
        >>> print(kwargs['submission_metadata'])
        {
            'status': u'running',
            'when_made_public': None,
            'participant_team': 5,
            'input_file': 'https://abc.xyz/path/to/submission/file.json',
            'execution_time': u'123',
            'publication_url': u'ABC',
            'challenge_phase': 1,
            'created_by': u'ABC',
            'stdout_file': 'https://abc.xyz/path/to/stdout/file.json',
            'method_name': u'Test',
            'stderr_file': 'https://abc.xyz/path/to/stderr/file.json',
            'participant_team_name': u'Test Team',
            'project_url': u'http://foo.bar',
            'method_description': u'ABC',
            'is_public': False,
            'submission_result_file': 'https://abc.xyz/path/result/file.json',
            'id': 123,
            'submitted_at': u'2017-03-20T19:22:03.880652Z'
        }
    """

    with open(test_annotation_file, 'r') as f:
        labels = f.readlines()
    with open(user_submission_file, 'r') as f:
        predictions = f.readlines()
    for i in range(len(labels)):
        labels[i] = int(labels[i].strip())
        predictions[i] = int(predictions[i].strip())
    if len(labels) != len(predictions):
        return 0
    positive_total = 0
    negative_total = 0
    positive_correct = 0
    negative_correct = 0
    total_correct = 0
    for i in range(len(labels)):
        if labels[i] == 1:
            positive_total += 1
        else:
            negative_total += 1
        if labels[i] == predictions[i]:
            if labels[i] == 1:
                positive_correct += 1
            else:
                negative_correct += 1
            total_correct += 1
    positive = positive_correct / positive_total
    negative = negative_correct / negative_total
    total = total_correct / len(labels)  
    output = {}
    if phase_codename == "dev":
        print("Evaluating for Dev Phase")
        output["result"] = [
            {
                "train_split": {
                    "Positive": positive,
                    "Negative": negative,
                    "Total": total,
                }
            }
        ]
        # To display the results in the result file
        output["submission_result"] = output["result"][0]["train_split"]
        print("Completed evaluation for Dev Phase")
    elif phase_codename == "test":
        print("Evaluating for Test Phase")
        output["result"] = [
            {
                "train_split": {
                    "Positive": positive,
                    "Negative": negative,
                    "Total": total,
                }
            },
            {
                "test_split": {
                    "Positive": positive,
                    "Negative": negative,
                    "Total": total,
                }
            },
        ]
        # To display the results in the result file
        output["submission_result"] = output["result"][0]
        print("Completed evaluation for Test Phase")
    return output
