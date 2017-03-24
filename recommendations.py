# A dictionary of movie critics and their ratings of a small set of movies

critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 2.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'The Night Listener': 3.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5},
    'Toby': {
        'Snakes on a Plane':4.5,
        'You, Me and Dupree':1.0,
        'Superman Returns':4.0
    }
}

ratings = {
    'John': {
      'Kong': 7.0,
      'John Wick': 7.5,
      'Logan': 6.0,
      'Split': 5.5,
      'Moana': 6.5,
      'La La La Land': 8.0
    },
    'Lee': {
      'Kong': 6.5,
      'John Wick': 5.0,
      'Logan': 4.5,
      'Split': 4,
      'La La La Land': 6.0,
      'Moana': 7.0
    },
    'Jacob': {
      'Kong': 6.0,
      'John Wick': 5.0,
      'Split': 7.0,
      'La La La Land': 8.0
    },
    'Sarah': {
      'John Wick': 7.0,
      'Logan': 6.0,
      'La La La Land': 9.5,
      'Split': 8.0,
      'Moana': 5.0
    },
    'Prince': {
      'Kong': 6.0,
      'John Wick': 8.0,
      'Logan': 5.0,
      'Split': 6.0,
      'La La La Land': 7.0,
      'Moana': 5.0
    },
    'Kevin': {
      'Kong': 7.0,
      'John Wick': 8.0,
      'La La La Land': 7.0,
      'Split': 10.0,
      'Moana': 7.5
    },
    'Jack': {
      'John Wick': 9.0,
      'Moana': 4.0,
      'Split':8.0
    }
  }


from math import sqrt
import pdb

# Return distance-based similarity score for person 1 and person 2
def sim_distance(prefs, person1, person2):
    # Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

    #if they have no rating in common, return 0
    if len(si) == 0: return 0

    #Add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1/(1 + sum_of_squares)

def sim_pearson(prefs, p1, p2):
    #Get list of mutally rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1

    #Find the number of elements
    n = len(si)

    # return 0 if they are no rating in common
    if n == 0: return 0

    '''Add up all the preferences'''
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    '''Sum up all the squares'''
    sum1Sq = sum([pow(prefs[p1][it],2 ) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2 ) for it in si])

    '''Sum up the products'''
    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])

    '''Calculate Pearson score'''
    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq - pow(sum1, 2)/n)*(sum2Sq - pow(sum2, 2)/n))
    if den == 0: return 0

    r = num/den

    return r

'''
Return the best matches for person from prefs dictionary.
Number of result and similarity function are optional params.
'''
def topMatches(prefs, person, n = 5, similarity = sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]

    '''Sort the list so the highest scores appear at the top'''
    scores.sort()
    scores.reverse()
    return scores[0:n]

'''
Gets recommendations for a person using weighted average of every other use's rating
'''
def getRecommendations(prefs, person, similarity = sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        '''Don't compare to yourself'''
        if other == person: continue
        sim = similarity(prefs, person, other)

        '''ignore scores if zero or lowers'''
        if sim <= 0: continue
        for item in prefs[other]:

            '''only score movies I haven't seen yet'''
            if item not in prefs[person] or prefs[person][item] == 0:
                '''Similarity * Score'''
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim

                '''Sum of similarities'''
                simSums.setdefault(item, 0)
                simSums[item] += sim

    '''Create the normalized list'''
    rankings = [(total/simSums[item], item) for item, total in totals.items()]

    ''' Return the sorted list'''
    rankings.sort()
    rankings.reverse()
    return rankings

'''
Transform source data
'''
def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            '''Flip item and person'''
            result[item][person] = prefs[person][item]

    return result

def calculateSimilarItems(prefs, n = 10):
    '''Create dictionary of items showing which other items they are most similar to'''
    result = {}

    '''Invert the preference matix to be item-centric'''
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        '''Status updates for large dataset'''
        c += 1
        if c%100 == 0: print "%d / %d " % (c, len(itemPrefs))
        '''Find the most similar items to this one'''
        scores = topMatches(itemPrefs, item, n = n, similarity = sim_distance)
        result[item] = scores

    return result

def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    '''Loop over items rated by this user'''
    for (item, rating) in userRatings.items():

        '''Loop over items similar to this one'''
        for (similarity, item2) in itemMatch[item]:

            '''Ignore if this user has already rated this item'''
            if item2 in userRatings: continue

            '''Weighted sum of rating times similarity'''
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            '''Sum of all the similarities'''
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    '''Divide each total score by total weighting to get an average'''
    rankings = [(score/totalSim[item], item) for item,score in scores.items()]

    '''return the rankings from highest to lowest'''
    rankings.sort()
    rankings.reverse()
    return rankings
