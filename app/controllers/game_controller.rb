class GameController < ApplicationController
  def index

    # 0: random
    # 1: pattern
    @game_level = params[:level] ? params[:level]: "0"

    if session[:level]
      @game_level = session[:level]
      session[:level] = nil
    end

    session[@game_level]||={}
    session[@game_level]['turn']||='pre'
    session[@game_level]['board']||= Game.initialize_board

    board = session[@game_level]['board']
    turn  = session[@game_level]['turn']
    sign = (turn == 'pre') ? 1 : -1

    p board

    case sign
    when 1
      if (params[:i] && params[:j])
        board, status = Game.user_action(board, params, sign)
        if status
          session[@game_level]["board"] = Game.ai_action(board, @game_level, sign)
        end
      end
    when -1
      if session[@game_level]['turn_first']
        session[@game_level]['board'] = Game.ai_action(board, @game_level, sign)
        session[@game_level]['turn_first'] = false
      else
        if (params[:i] && params[:j])
          board, status = Game.user_action(board, params, sign)
          if status
            session[@game_level]['board'] = Game.ai_action(board, @game_level, sign)
          end
        end
      end
    end

    # TODO rewrite
    case Game.status(board)
    when true
      @status = 'full'
    when Game::PRIMARY_SIGN
      @status = (turn == 'pre') ? 'win' : 'lose'
    when Game::SECONDARY_SIGN
      @status = (turn == 'pre') ? 'lose' : 'win'
    else
      # nothing to do
    end


  end

  def reset
    # reset_session
    l = params[:level]
    session[l]['turn'] = nil
    session[l]['turn'] = params[:turn] if params[:turn]
    session[l]['board']= nil

    session[l]['turn_first'] = true

    session[:level] = l

    redirect_to action: :index
  end

end
