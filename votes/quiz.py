from collections import Counter

PERFECT = 'perfect'
BEST = 'best'

def determine(data, results):
    if not results:
        raise ValueError("Need at least one result to use")

    system_votes = Counter()
    system_opportunities = Counter()
    for question_id, answer_id in results.items():
        if question_id not in data['questions']:
            continue
        elif answer_id == 'ignore':
            continue

        answers = data['questions'][question_id]['answers']
        if answer_id not in answers:
            continue

        for sys in answers[answer_id]['systems']:
            system_votes[sys] += 1

        for answer in answers.values():
            for sys in answer['systems']:
                system_opportunities[sys] += 1

    votes = []
    for sys in data['systems']:
        if system_opportunities[sys] > 0:
            votes.append((system_votes[sys] / system_opportunities[sys], sys))
    votes.sort()

    if not votes:
        raise ValueError("No votes counted")

    perfect = []
    best = []
    for vote in votes:
        if vote[0] == 1:
            perfect.append(vote)
        elif perfect:
            break
        elif not best or vote[0] >= best[0][0]:
            best.append(vote)
        else:
            break

    if perfect:
        return PERFECT, [i[1] for i in perfect], votes
    else:
        return BEST, [i[1] for i in best], votes
