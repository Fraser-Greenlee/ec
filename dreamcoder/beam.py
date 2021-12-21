'''
    Uses beam search to solve tasks.
'''
from dreamcoder.likelihoodModel import AllOrNothingLikelihoodModel
from dreamcoder.grammar import *
from dreamcoder.utilities import get_root_dir

import os
import traceback
import subprocess


def beamForTasks(g, tasks, likelihoodModel, _=None,
                      verbose=False,
                      timeout=None,
                      elapsedTime=0.,
                      CPUs=1,
                      testing=False, #unused
                      evaluationTimeout=None,
                      lowerBound=0.,
                      upperBound=100.,
                      budgetIncrement=1.0, maximumFrontiers=None):
    assert timeout is not None, \
        "beamForTasks: You must provide a timeout."

    from time import time

    request = tasks[0].request
    assert all(t.request == request for t in tasks), \
        "beamForTasks: Expected tasks to all have the same type"

    maximumFrontiers = [maximumFrontiers[t] for t in tasks]
    # store all of the hits in a priority queue
    # we will never maintain maximumFrontier best solutions
    hits = [PQ() for _ in tasks]

    starting = time()
    previousBudget = lowerBound
    budget = lowerBound + budgetIncrement

    import pdb
    pdb.set_trace()

    try:
        totalNumberOfPrograms = 0
        while time() < starting + timeout and \
                any(len(h) < mf for h, mf in zip(hits, maximumFrontiers)) and \
                budget <= upperBound:
            numberOfPrograms = 0

            for prior, _, p in g.enumeration(Context.EMPTY, [], request,
                                             maximumDepth=99,
                                             upperBound=budget,
                                             lowerBound=previousBudget):
                descriptionLength = -prior
                # Shouldn't see it on this iteration
                assert descriptionLength <= budget
                # Should already have seen it
                assert descriptionLength > previousBudget

                numberOfPrograms += 1
                totalNumberOfPrograms += 1

                for n in range(len(tasks)):
                    task = tasks[n]

                    #Warning:changed to max's new likelihood model situation
                    #likelihood = task.logLikelihood(p, evaluationTimeout)
                    #if invalid(likelihood):
                        #continue
                    success, likelihood = likelihoodModel.score(p, task)
                    if not success:
                        continue
                        
                    dt = time() - starting + elapsedTime
                    priority = -(likelihood + prior)
                    hits[n].push(priority,
                                 (dt, FrontierEntry(program=p,
                                                    logLikelihood=likelihood,
                                                    logPrior=prior)))
                    if len(hits[n]) > maximumFrontiers[n]:
                        hits[n].popMaximum()

                if timeout is not None and time() - starting > timeout:
                    raise EnumerationTimeout

            previousBudget = budget
            budget += budgetIncrement

            if budget > upperBound:
                break
    except EnumerationTimeout:
        pass
    frontiers = {tasks[n]: Frontier([e for _, e in hits[n]],
                                    task=tasks[n])
                 for n in range(len(tasks))}
    searchTimes = {
        tasks[n]: None if len(hits[n]) == 0 else \
        min(t for t,_ in hits[n]) for n in range(len(tasks))}

    return frontiers, searchTimes, totalNumberOfPrograms




