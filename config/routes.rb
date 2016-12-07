Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  root 'welcome#index'

  get 'game/lv0', controller: :game, action: 'lv0'
  get 'game/reset', controller: :game, action: 'reset'
  post 'game/lv0', controller: :game, action: 'lv0_post'
  resources :game
end
