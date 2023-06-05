# Week4 課題
## find_shortest_pathについて
* 以下の配列を用意した
  * queue
  * 訪問したnodeを格納する配列visited
  * あるnodeの1つ手前のnodeを格納する配列before
* queueが空になるまで以下の操作を繰り返す
  * あるnodeと繋がっているchild_nodeを取得
  * もしchild_nodeがgoalであれば, beforeを遡って最短経路を出力
  * child_nodeとgoalが異なっていればqueue, before, visitedを更新する

## find_most_popular_pagesについて
* 10000回の操作が終わるまで, あるいは1操作後の配列との差のノルムが0.1未満であれば終了する
* PR(A) = (1-d) + dΣ(PR(T_i)/C(T_i))の式に従っている