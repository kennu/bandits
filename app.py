import random
import sys
import numpy as np
import bandit

from sklearn.feature_extraction.text import HashingVectorizer

np.random.seed(1337)

vectorizer = HashingVectorizer(n_features=100)
contextual_bandit = bandit.epsilonGreedyContextualBandit()

# Example with three advertisments we would like to show
arms = ['advertisment_1', 'advertisment_2', 'advertisment_3', 'advertisment_4']

# The job of the bandit is to learn the true click-through rates
# of each arm, but for simulation purposes, we'll cheat and pretend 
# we already know.
ctrs = [0.4, 0.052, 0.0522, 0.0521]

# Simulate a single context, a male website visitor aged 21 that uses Firefox
context = vectorizer.fit_transform(['age_21 gender_male browser_firefox'])
counts = np.zeros(len(arms))

epochs = 100000
print('Running simulation for ' + str(epochs) + ' epochs')
for i in range(epochs):
    sys.stdout.write('.')
    sys.stdout.flush()
    chosen_arm = contextual_bandit.select_arm(context, arms)
    # Send reward based on our pretend CTR for the chosen arm:
    # - 1: clicked
    # - 0: not clicked
    if random.random() <= ctrs[arms.index(chosen_arm)]:
        contextual_bandit.reward(chosen_arm, context, 1)
    else:
        contextual_bandit.reward(chosen_arm, context, 0)
    counts[arms.index(chosen_arm)] += 1

print('done.\nResults:')
for i, v in enumerate(counts):
    print('Arm ' + arms[i] + ' was chosen ' + str(counts[i]) + ' times.')