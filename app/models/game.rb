class Game < ApplicationRecord
  def self.initialize_board
    9.times.map{|i| 9.times.map{|j| 0 } }
  end
end
