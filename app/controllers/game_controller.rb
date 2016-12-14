class GameController < ApplicationController
  def index

    # 0: random
    # 1: pattern
    @game_level = params[:level] ? params[:level]: "0" 

    session[@game_level]||={}
    session[@game_level]['turn']||='pre'
    session[@game_level]['board']||= Game.initialize_board

    status = Game.status(session[@game_level]['board'])

    if params[:i] && params[:j] && !status
      i, j = params[:i].to_i, params[:j].to_i
      if session[@game_level]['board'][i][j] == 0
        sign = (session[@game_level]['turn'] == 'pre') ? 1 : -1
        session[@game_level]['board'][i][j] = sign

        # true : full board
        # 1 | -1  : winner sign
        status = Game.status(session[@game_level]['board'])

        # turn of a counter
        unless status
          session[@game_level]["board"] = Game.ai(session[@game_level]['board'], @game_level, sign)
        end

      end
    end

    # TODO rewrite
    case status
    when true
      @status = 'full'
    when Game::PRIMARY_SIGN
      @status = session[@game_level]['turn'] == 'pre' ? 'win' : 'lose'
    when Game::SECONDARY_SIGN
      @status = session[@game_level]['turn'] == 'pre' ? 'lose' : 'win'
    else
      # nothing to do
    end

    p session[@game_level]

  end

  def reset
    # reset_session
    l = params[:level]
    session[l]['turn'] = nil
    session[l]['board']= nil

    redirect_to action: :index
  end

end
