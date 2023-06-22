# Week5-6 TSP問題

## week5 貪欲法の工夫(TSP.py)
* 盤面を近似的に時計回り/反時計回りに回るといいのではないかと考え, 盤面を4分割し, 斜め右下・斜め左下・斜め左上に重みをつけて距離を計算する関数を用意した
* 毎回, 次に進むノードを選ぶときに重みをつけて選んだ
  * 今いる頂点が盤面の斜右下にあるときは斜右下のノードに重みをつけて優先的に選ぶ...など

## Week6 アントコロニーを使ってみる(TSP2.py)
* アントコロニー最適化では、パラメーターとして以下のものがある
  * 蟻の数num_of_ants
  * 適当に決めるパラメーターQ
  * フェロモンの重視度α
  * ヒューリスティックの重視度β
  * フェロモンの最小値τmin
  * フェロモン最大値τmax
  * フェロモン蒸発率ρ
  * 最大イテレーション回数max_iterations
  * ランダムに次に進む頂点を選ぶ確率ant_prob_random
  * 局所解に陥ったことを確認するための数super_not_change
* パラメーターの数があまりにも多くて最適な撮り方がわからなかったので、 いくつかの参考文献をあたって試してみたが、手元のLaptopでは実行時間の問題があり思考を繰り返すことが難しかった. 最終的に, 以下のようにした. (蟻の数を10000まで増やすと精度は上がるが、N=2048などで計算が4時間以上回しても終わらなかったので、諦めた)
  * num_of_ants=100
  * Q=100
  * alpha=3
  * beta=2
  * rou=0.8
  * max_iterations=500
  * initial_vertex=0
  * tau_min=0
  * tau_max=100
  * ant_prob_random=0.1
  * super_not_change=30
* 上のパラメーターの取り方では, Nが100を超えると一気に精度が落ちたので, N>100の範囲では先週の関数を使って最短経路を求めることにした.
* 参考：
  * https://qiita.com/ganyariya/items/25824f1502478a673005
  * https://www.topic.ad.jp/ipsj-tohoku/archive/2009/report/2009-2-12.pdf