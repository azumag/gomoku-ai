class GameController < ApplicationController
  def index

    # 0: random
    # 1: pattern
    @game_level = params[:level] ? params[:level]: "0"


    session[@game_level]||={}
    session[@game_level]['turn']||='pre'
    session[@game_level]['board']||= Game.initialize_board

    sign = (session[@game_level]['turn'] == 'pre') ? 1 : -1

    case sign
    when 1
      session[@game_level]['board'] = Game.user_action(params, session[@game_level]['board'], status)
      session[@game_level]["board"] = Game.ai(session[@game_level]['board'], @game_level, sign)
    when -1
      session[@game_level]["board"] = Game.ai(session[@game_level]['board'], @game_level, sign)
      session[@game_level]['board'] = Game.user_action(params, session[@game_level]['board'], status)
    end

    # TODO rewrite
    case Game.status(session[@game_level]['board'])
    when true
      @status = 'full'
    when Game::PRIMARY_SIGN
      @status = session[@game_level]['turn'] == 'pre' ? 'win' : 'lose'
    when Game::SECONDARY_SIGN
      @status = session[@game_level]['turn'] == 'pre' ? 'lose' : 'win'
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

    redirect_to action: :index
  end

end
