class Game < ApplicationRecord

  BOARD_SIZE = 9
  WIN_SIZE   = 5

  PRIMARY_SIGN   = 1
  SECONDARY_SIGN = -1

  def self.initialize_board
    BOARD_SIZE.times.map{|i| BOARD_SIZE.times.map{|j| 0 } }
  end

  def self.user_action(board, param, sign, status)

    status = nil
    if (params[:i] && params[:j] && !status)
      i, j = params[:i].to_i, params[:j].to_i
      if board[i][j] == 0
        board[i][j] = sign

        # true : full board
        # 1 | -1  : winner sign
        status = Game.status(board)
      end
    end

    return board, status

  end

  def self.ai(board, level, sign, status)
    while true
      case level
      when '0'
        # RANDOM AI
        i, j = rand(BOARD_SIZE), rand(BOARD_SIZE)
      when '1'
        i, j = rand(BOARD_SIZE), rand(BOARD_SIZE)
      end

      if board[i][j] == 0
        board[i][j] = sign *- 1
        break
      end

      status = Game.status(board)
      break if status

    end

    board

  end

  def self.status(board)

    # Check win/lose
    board.each_with_index do |ii, i|
      ii.each_with_index do |jj, j|
        next if jj == 0
        return jj if self.check_win(board, jj, i, j)
      end
    end

    # Check board full
    finished = true
    board.each do |ii|
      ii.each do |jj|
        if (jj == 0)
          finished = false
          break
        end
      end
    end

    finished
  end

  def self.check_win(board, sign, i, j)
    cnt = 0
    ## tate check
    WIN_SIZE.times do |w|
      break if j+WIN_SIZE > BOARD_SIZE
      break if board[i][j+cnt] != sign
      cnt += 1
    end
    check = (cnt >= WIN_SIZE)
    return true if check

    cnt = 0
    ## yoko check
    WIN_SIZE.times do |w|
      break if i+WIN_SIZE > BOARD_SIZE
      break if board[i+cnt][j] != sign
      cnt += 1
    end
    check = (cnt >= WIN_SIZE)
    return true if check


    cnt = 0
    ## naname check forward
    WIN_SIZE.times do |w|
      break if i+cnt > BOARD_SIZE
      break if j+cnt > BOARD_SIZE
      break unless board[i+cnt]
      break unless board[i+cnt][j+cnt]
      break if board[i+cnt][j+cnt] != sign
      cnt += 1
    end
    check = (cnt >= WIN_SIZE)
    return true if check

    cnt = 0
    ## naname check backward
    WIN_SIZE.times do |w|
      break if i+cnt < 0
      break if j-cnt < 0
      break unless board[i+cnt]
      break unless board[i+cnt][j-cnt]
      break if board[i+cnt][j-cnt] != sign
      cnt += 1
    end
    check = (cnt >= WIN_SIZE)
    return true if check

  end

end
