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
