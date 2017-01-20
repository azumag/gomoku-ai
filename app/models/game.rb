class Game < ApplicationRecord
  require 'open3'

  BOARD_SIZE = 9
  WIN_SIZE   = 5

  PRIMARY_SIGN   = 1
  SECONDARY_SIGN = -1

  PSEUDO_INF_LOOP = 1000000 ## to prevent infinite loop

  WEIGHT_FOR_AVOID = 6
  FIXNUM_MAX = (2**(0.size * 8 -2) -1)

  REACH_SIZE = 3

  def self.initialize_board
    BOARD_SIZE.times.map{|i| BOARD_SIZE.times.map{|j| 0 } }
  end

  def self.user_action(board, params, sign)
    status = Game.status(board)
    if !status
      i, j = params[:i].to_i, params[:j].to_i
      if board[i][j] == 0
        board[i][j] = sign
        status = true
      end
    end
    return board, status
  end

  def self.ai_action(board, level, sign)
    self_sign = sign*-1
    if !Game.status(board) # proceed if not finished

      failed = false

      PSEUDO_INF_LOOP.times do
        # 初手なら適当に置く
        first_turn = board.flatten.reject{|b| b==0||b==sign }.empty?
        level = '0' if first_turn && level.to_i < 5

        # level change if location is fail
        if failed 
          level = '0' 
          failed = false
        end

        case level
        when '0'
          # RANDOM AI
          i, j = Game.random_indices
        when '1'
          # 旧型 IF THEN 系 AI
          # * lv-1 自分の周りの開いているマスに置く
          i, j = Game.search_round_empty(board, self_sign)
        when '2'
          # lv-2 もっとも価値の高い場所に置く（盤面評価）
          # でもてきとー, １段階なので先読みなし
          # 評価項目：
          # / 縦横斜どこに今一番ならべられているかで置く方向を決める
          maxreward = 0
          maxreward_index = random_indices
          BOARD_SIZE.times do |i|
            BOARD_SIZE.times do |j|
              next if board[i][j] != 0
              reward = calc_reward_for_num(board, i, j, sign, self_sign)
              if reward >= maxreward
                maxreward = reward
                maxreward_index = [i, j]
              end
            end
          end
          i, j = maxreward_index[0], maxreward_index[1]
        when '3'
          # lv 1+2
          maxreward = 0
          maxreward_index = random_indices
          BOARD_SIZE.times do
            i, j = Game.search_round_empty(board, self_sign)
            reward = calc_reward_for_num(board, i, j, sign, self_sign)
            if reward >= maxreward
              maxreward = reward
              maxreward_index = [i, j]
            end
          end
          i, j = maxreward_index[0], maxreward_index[1]

        when '4'
          # lv 1+2+
          # 相手が並べそうになったら邪魔をする
          # それ以外は自分の周りの価値の高い場所へ置く
          maxreward = 0
          maxreward_index = random_indices
          BOARD_SIZE.times do |i|
            BOARD_SIZE.times do |j|
              next if board[i][j] != 0
              reward = calc_reward_for_avoid(board, i, j, sign, self_sign)
              if reward >= maxreward
                maxreward = reward
                maxreward_index = [i, j]
              end
            end
          end
          BOARD_SIZE.times do
            i, j = Game.search_round_empty(board, self_sign)
            reward = calc_reward_for_num(board, i, j, sign, self_sign)
            if reward >= maxreward
              maxreward = reward
              maxreward_index = [i, j]
            end
          end
          i, j = maxreward_index[0], maxreward_index[1]
        when '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'
            # lv 5  using machine learning: 2-layer NN
            # lv 6  3-layer NN
            # lv 7  cnn 3-layer
            # lv 8  4-layer nn
            # lv 9  inf 4l nn - from initial
            # lv 10  inf 4l nn - from educated
            # lv 11 inf ?
            # lv 12 inf cnn - f edu
            # lv 13 inf 2lnn - f edu
            # lv 14 inf cnn randoms(0-14) f edu
            # lv 15 inf cnn vs random f edu
         
            result = nil
            puts self_sign
            puts_as_txt(board)
            inv = board.flatten.map{|a| a.to_i * self_sign}
            board_bridge = inv.map{|a| (a.to_i==SECONDARY_SIGN) ? 2 : a.to_i}.join(' ')
            cmd = "python #{Rails.root}/ai/lv#{level}/exe.py #{board_bridge}"
            p cmd
            result, e, s = Open3.capture3(cmd)
            p result
            p e
            #p s
            i = (result.to_i/BOARD_SIZE).to_i
            j = (result.to_i - BOARD_SIZE*i)
            puts i,j
        end

        if board[i][j] == 0
          board[i][j] = self_sign
          break
        end

        status = Game.status(board)
        break if status

        failed = true

      end
    end

    board

  end

  # true : full board
  # 1 | -1  : winner sign
  def self.status(board)

    # Check win/lose
    board.each_with_index do |ii, i|
      ii.each_with_index do |sign, j|
        next if sign == 0
        return sign if self.check_win(board, sign, i, j)
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
    # TODO : refactoring
    cnt = 0
    ## horizontal check
    WIN_SIZE.times do |w|
      break if j+WIN_SIZE > BOARD_SIZE
      break if board[i][j+cnt] != sign
      cnt += 1
    end
    check = (cnt >= WIN_SIZE)
    return true if check

    cnt = 0
    ## vertical check
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

  def self.random_indices
    return rand(BOARD_SIZE), rand(BOARD_SIZE)
  end

  def self.search_round_empty(board, self_sign)
    found = false
    PSEUDO_INF_LOOP.times do
      i, j = Game.random_indices
      if board[i][j] == self_sign # ランダムに自分の石を探す
        seek = []
        found = false
        PSEUDO_INF_LOOP.times do
          n_around = 6
          dice = rand(n_around)
          # TODO: sophisticate
          case dice
          when 0
            if board[i] && board[i][j+1] == 0
              found = [i, j+1]
            end
          when 1
            if board[i] && board[i][j-1] == 0
              found = [i, j-1]
            end
          when 2
            if board[i-1] && board[i-1][j+1] == 0
              found = [i-1, j+1]
            end
          when 3
            if board[i-1] && board[i-1][j-1] == 0
              found = [i-1, j-1]
            end
          when 4
            if board[i+1] && board[i+1][j+1] == 0
              found = [i+1, j+1]
            end
          when 5
            if board[i+1] && board[i+1][j-1] == 0
              found = [i+1, j+1]
            end
          end
          break if found
          seek << dice
          break if (seek.uniq.size >= n_around)
        end
      end
      break if found
    end

    if found
      return found[0], found[1]
    else
      return Game.random_indices
    end
  end

  def self.calc_reward_for_avoid(board, i, j, sign, self_sign)

    max_h_chain = Game.check_horizontal_warn(board, sign, i, j)
    max_v_chain = Game.check_vertical_warn(board, sign, i, j)
    max_t_chain = Game.check_tilt_warn(board, sign, i, j)

    reward = 0
    reward += max_h_chain
    reward += max_v_chain
    reward += max_t_chain

    reward *= 4

    reward = FIXNUM_MAX if max_h_chain == 5
    reward = FIXNUM_MAX if max_v_chain == 5
    reward = FIXNUM_MAX if max_t_chain == 5

    if max_h_chain > 0 || max_v_chain > 0 || max_t_chain > 0
     # puts "------"
     # p max_h_chain
     # p max_v_chain
     # p max_t_chain
    end

    return reward
  end

  def self.calc_reward_for_num(board, i, j, sign, self_sign)

    horizontals, verticals, tilts_f, tilts_b = breakdown_board(board, i, j)

    my_horizontal = horizontals.select{|b| b == self_sign}.size
    my_vertical   = verticals.select{|b| b == self_sign}.size
    my_tilt        = tilts_f.select{|b| b == self_sign}.size
    my_tilt       += tilts_b.select{|b| b == self_sign}.size


    en_horizontal = horizontals.select{|b| b == sign}.size
    en_vertical   = verticals.select{|b| b == sign}.size
    en_tilt        = tilts_f.select{|b| b == sign}.size
    en_tilt       += tilts_b.select{|b| b == sign}.size

    reward = (my_horizontal + my_vertical + my_tilt) + (en_horizontal + en_vertical + en_tilt)

    if (i == j) && i == 0
      #puts "#{i}, #{j}'----------------------'"
      #puts "#{my_horizontal} --- #{my_vertical} --- #{my_tilt}"
      #puts "#{en_horizontal} --- #{en_vertical} --- #{en_tilt}"
      #puts "#{horizontals}, #{verticals}, #{tilts_f}, #{tilts_b}"
    end

    return reward
  end

  def self.calc_chain(target_line, sign, k)
    chain = 0
    max_chain = 0
    # forward
    WIN_SIZE.times do |w|
      targ_idx = (k+(w+1))
      break if targ_idx >= target_line.size
      t = target_line[targ_idx]
      if t == sign
        chain += 1
      else
        break
      end
    end
    # backward
    WIN_SIZE.times do |w|
      targ_idx = (k-(w+1))
      break if targ_idx < 0
      t = target_line[targ_idx]
      if t == sign
        chain += 1
      else
        break
      end
    end

    return chain
  end

  def self.breakdown_board(board, i, j)

    horizontals = []
    cnt = 0
    board[i].each_with_index do |col, l|
      next if l < j
      horizontals << col
    end
    cnt = 0
    board[i].each_with_index do |col, l|
      break if l > j
      horizontals << col
    end

    verticals = []
    board.each_with_index do |row, l|
      next if l < i
      verticals << row[j]
    end
    board.each_with_index do |row, l|
      break if l > i
      verticals << row[j]
    end

    tilts_f = []
    cnt = 0
    board.each_with_index do |row, l|
      next if l < i
      row.each_with_index do |col, n|
        next if n < j+cnt
        tilts_f << col
        cnt += 1
        break
      end
    end
    cnt = 0
    board.each_with_index do |row, l|
      break if l > i
      row.each_with_index do |col, n|
        break if n > j-cnt
        if n == j-cnt
          tilts_f << col
          cnt += 1
          break
        end
      end
    end

    cnt = 0
    tilts_b = []
    board.each_with_index do |row, l|
      next if l < i
      row.each_with_index do |col, n|
        next if n < (j - cnt)
        tilts_b << col
        cnt += 1
        break
      end
    end
    # TODO ; check vigorously
    cnt = 0
    board.each_with_index do |row, l|
      break if l > i
      row.each_with_index do |col, n|
        next if n < (j + cnt)
        tilts_b << col
        cnt += 1
        break
      end
    end
    return board[i], verticals, tilts_f, tilts_b
  end

  def self.check_horizontal_warn(board, sign, i, j)
    # TODO: sophistication
    cnt = 1
    ## forward
    REACH_SIZE.times do |w|
      break unless board[i][j+cnt]
      break if board[i][j+cnt] != sign
      cnt += 1
    end
    check = (cnt-1 >= REACH_SIZE)
    return cnt if check

    cnt = 1
    ## backward
    WIN_SIZE.times do |w|
      break unless board[i][j-cnt]
      break if board[i][j-cnt] != sign
      cnt += 1
    end
    check = (cnt-1 >= REACH_SIZE)
    return cnt if check
    return 0
  end

  def self.check_vertical_warn(board, sign, i, j)
    # TODO: sophistication
    ## vertical check
    # forward
    cnt = 1
    WIN_SIZE.times do |w|
      break unless board[i+cnt]
      break if board[i+cnt][j] != sign
      cnt += 1
    end
    check = (cnt-1 >= REACH_SIZE)
    return cnt if check

    # backward
    cnt = 1
    WIN_SIZE.times do |w|
      break unless board[i-cnt]
      break if board[i-cnt][j] != sign
      cnt += 1
    end
    check = (cnt-1 >= REACH_SIZE)
    return cnt if check
    return 0
  end

  def self.check_tilt_warn(board, sign, i, j)
    # TODO: sophistication
    cnt = 1
    ## naname check forward
    WIN_SIZE.times do |w|
      break if i+cnt > BOARD_SIZE
      break if j+cnt > BOARD_SIZE
      break unless board[i+cnt]
      break unless board[i+cnt][j+cnt]
      break if board[i+cnt][j+cnt] != sign
      cnt += 1
    end
    check = (cnt-1 >= REACH_SIZE)
    return cnt if check

    ## naname check forward-back
    cnt = 1
    WIN_SIZE.times do |w|
      break if i-cnt < 0
      break if j-cnt < 0
      break unless board[i-cnt]
      break unless board[i-cnt][j-cnt]
      break if board[i-cnt][j-cnt] != sign
      cnt += 1
    end
    check = (cnt-1 >= REACH_SIZE)
    return cnt if check

    cnt = 1
    ## naname check backward
    WIN_SIZE.times do |w|
      break if i+cnt > BOARD_SIZE
      break if j-cnt < 0
      break unless board[i+cnt]
      break unless board[i+cnt][j-cnt]
      break if board[i+cnt][j-cnt] != sign
      cnt += 1
    end
    check = (cnt >= REACH_SIZE)
    return cnt if check

    cnt = 1
    ## naname check backward-back
    WIN_SIZE.times do |w|
      break if i-cnt < 0
      break if j+cnt > BOARD_SIZE
      break unless board[i-cnt]
      break unless board[i-cnt][j+cnt]
      break if board[i-cnt][j+cnt] != sign
      cnt += 1
    end
    check = (cnt >= REACH_SIZE)
    return cnt if check


    return 0

  end

  def self.generate_histories(lp, game_level_prime, game_level_second, log, mode='w', rn=false)
      game_level_prime = game_level_prime.to_s
      game_level_second = game_level_second.to_s
      level = game_level_prime
      wins = {}
      wins[PRIMARY_SIGN] = 0
      wins[SECONDARY_SIGN] = 0
      p wins
      game_cnt = 0
      lp.times do |i|
          begin
              puts "history - #{i}"
              if rn
                  puts '-----------'
                  p rand
                  if rand > 0.5
                      level = rand(14).to_s
                  else
                      level  = game_level_prime
                  end
		  level = '0' if rn == 0
                  p level
              end
              hist, answ , win = self.generate_history(level, game_level_second)
              if hist && answ
                  wins[win] += 1 
                  game_cnt += 1
                  next if log.blank?
                  logpath = log
                  sign = answ.first.max>0 ? PRIMARY_SIGN : SECONDARY_SIGN
                  f = File.open('ai/tmp/h-'+log, mode)
                  hist.each do |his|
                      inv = his.map{|a| a.to_i * sign }
                      f.puts inv.map{|a| (a.to_i==SECONDARY_SIGN) ? 2 : a.to_i}.join(',')
                  end
                  f.close
                  f = File.open('ai/tmp/a-'+log, mode)
                  answ.each do |ans|
                      f.puts ans.map{|a| a.to_i * sign}.join(',')
                  end
                  f.close
              end
          rescue => e
              puts e.backtrace
          end
      end
      p wins
      p wins[PRIMARY_SIGN] / game_cnt.to_f
      p wins[SECONDARY_SIGN] / game_cnt.to_f
  end


  def self.puts_as_txt(board)
      cnt = 0
      board.flatten.each do |j|
          cnt += 1
          print 'O' if j == PRIMARY_SIGN
          print 'X' if j == SECONDARY_SIGN
          print '+' if j == 0
          puts "\n" if cnt.modulo(BOARD_SIZE) == 0
      end
  end

  def self.generate_history(game_level_p, game_level_s) 
    board = Game.initialize_board

    board_histories = []
    answr_histories = {}

    39.times do |t|
        puts "----#{t}----"
        #cnt = 0
        #board.flatten.each do |j|
        #    cnt += 1
        #    print 'O' if j == PRIMARY_SIGN
        #    print 'X' if j == SECONDARY_SIGN
        #    print '+' if j == 0
        #    puts "\n" if cnt.modulo(BOARD_SIZE) == 0
        #end
        [PRIMARY_SIGN, SECONDARY_SIGN].each do |sign|
        board_histories[t] = board.flatten
        tmp_board = Marshal.load(Marshal.dump(board))
        game_level = (sign==PRIMARY_SIGN) ? game_level_p : game_level_s
        next_board = Game.ai_action(tmp_board, game_level, sign*-1)
        (answr_histories[sign]||=[]) << diff(board_histories[t], next_board.flatten, sign)
        case Game.status(next_board)
        when true
          # draw
          puts 'draw'
          return nil
        when sign
          #board_histories.each_with_index do |bh, i|
           # cnt = 0
           #puts "===c==="
            #cnt = 0
            #answr_histories[sign][i].each do |j|
            #  cnt += 1
            #  object = sign==PRIMARY_SIGN ? "O" : "X"
            #  print object if j == 1
            #  print '+' if j == 0
            #  puts "\n" if cnt.modulo(BOARD_SIZE) == 0
            #end
          #end
          return board_histories, answr_histories[sign], sign
        else
         board = next_board
        end
      end
    end
    puts 'not end'
    return nil

  end

  def self.diff(src, dst, sign)
    ret = Array.new(src.size, 0)
    src.each_with_index do |s, i|
      if s != dst[i]
        ret[i] = sign
        return ret
      end
    end
    return ret
  end

  def self.train_infinite(batch, level, log='inf', mode='new', rn=false)
      case mode
      when 'new'
          while true
             generate_histories(batch, level, level, log, 'a', rn)
              cmd = "python #{Rails.root}/ai/lv#{level}/train.py #{log}"
              result, e, s = Open3.capture3(cmd)
              p result, e

              begin
              File.delete("#{Rails.root}/ai/tmp/h-#{log}")
              File.delete("#{Rails.root}/ai/tmp/a-#{log}") 
              rescue => e
                  puts e
              end

          end
      end
  end

end
