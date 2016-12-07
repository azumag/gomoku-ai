class GameController < ApplicationController
  def index

  end

  def lv0
    session[:turn]||='pre'
    session[:board]||= Game.initialize_board

    if params[:i] && params[:j]
      i, j = params[:i].to_i, params[:j].to_i
      if session[:board][i][j] == 0
        sign = (session[:turn] == 'pre') ? 1 : -1
        session[:board][i][j] = sign

        while true
          rndi, rndj = rand(9), rand(9)
          if session[:board][rndi][rndj] == 0
            session[:board][rndi][rndj] = sign *- 1
            break
          end

          finished = true
          session[:board].each do |ii|
            ii.each do |jj|
              if (jj == 0)
                finished = false
                break
              end
            end
          end
          break if finished
        end


      end
    end
  end

  def reset
    session[:turn] = nil
    session[:board]= nil

    redirect_to action: :lv0
  end

end
