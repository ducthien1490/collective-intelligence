require 'pry'

RATINGS = {
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

def euclidean_distance data, ref_1, ref_2
  # return 0 if ref_1 or ref2_ not exist in data
  return 0 unless data[ref_1] || data[ref_2]

  #Get the common items
  similar = []
  data[ref_1].each do |item_key, item_val|
    if data[ref_2][item_key]
      similar.push item_key
    end
  end

  # return 0 if there're no common
  return 0 if similar.length == 0

  # Sum all squares of dirrerences
  sum_squares_diff = data[ref_1].map do |k, v|
    next unless data[ref_2]
    (data[ref_1][k] - data[ref_2][k])**2
  end.compact.sum

  1/(1 + sum_squares_diff)
end

def pearson_correlation data, ref_1, ref_2
  # return 0 if ref_1 or ref2_ not exist in data
  return 0 unless data[ref_1] || data[ref_2]

  #Get the common items
  similar = []
  data[ref_1].each do |item_key, item_val|
    if data[ref_2][item_key]
      similar.push item_key
    end
  end

  #counting number of common items
  item_num = similar.length

  # return 0 if there're no common
  return 0 if item_num == 0

  #Add up all common item rating
  sum_ref_1 = similar.map{|c_i| data[ref_1][c_i] }.sum
  sum_ref_2 = similar.map{|c_i| data[ref_2][c_i] }.sum

  #Add up all square of common item rating
  sum_square_ref_1 = similar.map{|c_i| data[ref_1][c_i]**2 }.sum
  sum_square_ref_2 = similar.map{|c_i| data[ref_2][c_i]**2 }.sum

  #Sum all the products of common rating
  products_sum = similar.map{|c_i| data[ref_1][c_i]*data[ref_2][c_i]}.sum

  #Calculate Pearson Score
  num = products_sum - sum_ref_1*sum_ref_2/item_num
  den = Math.sqrt((sum_square_ref_1 - sum_ref_1**2/item_num)*
                  (sum_square_ref_2 - sum_ref_2**2/item_num))
  return 0 if den == 0
  num/den
end

def top_matches data, user, n = 5
  scores = data.map do |member, _|
    next if user == member
    #In this case, I use Pearson score
    {}.tap do |member_rating|
      member_rating[member] = pearson_correlation(data, user, member)
    end
  end.compact

  #Sort the list to get the highest score
  scores.sort_by{|user_rating| user_rating.values.first }.reverse.take(n)
end

def user_based_recommendation data, user
  totals = {}
  sim_sum = {}
  data.each do |member, rating|
    #Skip if member is user
    next if member == user

    sim_score = pearson_correlation(data, user, member)
    next if sim_score <= 0
    rating.each do |movie, rate|
      #only score movies that user haven't seen yet
      if data[user][movie].nil? || data[user][movie] == 0
        #Similarity * score
        totals[movie] = 0 if totals[movie].nil?
        totals[movie] += (data[member][movie] * sim_score)

        #Sum of similarities
        sim_sum[movie] = 0 if sim_sum[movie].nil?
        sim_sum[movie] += sim_score
      end
    end
  end

  rankings = totals.map do |re_movie, re_score|
    {}.tap do |recommendation|
      recommendation[re_movie] = totals[re_movie]/sim_sum[re_movie]
    end
  end
  rankings.sort_by{|rank| rank.values.first }.reverse
end
