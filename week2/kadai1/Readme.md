# hash_table.pyについて
## 用意した配列:
* bucket_size_list
  * ハッシュテーブルのバケットサイズの候補をいくつか格納したリスト. 全て要素が素数になるようにし, また値が互いの2-3倍になるようにした. 今回は, 最終的に挿入するデータの量が最大でも10000であることがわかっているので, リストの最大の要素は104729になっている.

今回は, 登録される文字列に含まれるのが小文字アルファベットと数字だけだとわかっているので, 小文字アルファベットと数字に対して素数を割り当てるような行列を用意した.
* prime_list_alphabet
  * 各アルファベットに対して素数を一つずつ割り当てた. 基本的には素数の小さい順にaから割り当てているが, 2は割り当てないこととと, bucket_size_listに含まれている要素は割り当てないように注意した.
* prime_list_number
  * 各数字に対して素数を一つずつ割り当てた. prime_list_alphabetで割り当てた素数の続きから小さい順に割り当てていき, ここでもbuclet_size_listにすでに含まれている要素は割り当てないようにした.

## 用意した構造
* Item
  * key: アイテムのキー. 文字列で表される.
  * value: アイテムの値.
  * next: 連結リストの次のアイテムを指定する. そのアイテムが最後尾の場合はNoneになる.
* HashTable
  * bucket_index : bucket_size_listで現在使用しているインデックス
  * self.bucket_size: バケットの大きさ
  * self.buckets: バケットのリスト. self.buckets[hash % self.bucket_size]はハッシュ値がhashであるような値の連結リストを格納している
  * self.item_count: ハッシュテーブルの中の要素の合計

## 用意した関数
* size_notification(self)
  * ハッシュテーブルに含まれている要素数が, ハッシュテーブルの大きさの70%を超えたら2を返す
  * ハッシュテーブルに含まれている要素数が, ハッシュテーブルの大きさの30%を下回ったら1を返す
  * それ以外の時は0を返す
* def rehash_expand(self)
  * サイズを大きくしたハッシュテーブルを新しく作り, 元々のデータを全て移して返す関数
  * もしbucket_size_listにそれ以上のサイズが格納されていない場合, 元のハッシュテーブルを返す
  * 新しいハッシュテーブルnew_hash_tableを作り, 参照するbucket_size_listのインデックスを元のハッシュテーブルに1を足して, 対応するサイズのバケットを作る
  * 元のハッシュテーブルのバケットを全て探索し, 格納されているデータを新しくハッシュしなおしてnew_hash_tableに格納する
* rehash_reduce(self)
  * サイズを小さくしたハッシュテーブルを新しく作り, 元々のデータを全て移して返す関数
  * もしbuclet_size_listにそれ以下のサイズが格納されていない場合, 元のハッシュテーブルを返す
  * 新しいハッシュテーブルnew_hash_tableを作り, 参照するbucket_size_listのインデックスを元のハッシュテーブルから1を引いて, 対応するサイズのバケットを作る
  * 元のハッシュテーブルのバケットを全て探索し, 格納されているデータを新しくハッシュしなおしてnew_hash_tableに格納する
* calculate_hash(key)
  * ハッシュ値を計算する関数
  * アルファベットであれば, prime_list_alphabetで対応づけられた素数を足していく
  * 数字であれば, prime_list_numberで対応づけられた素数を足していく
* put(self, key, value)
  * 新しいキーと値の組を登録する関数
  * キーが文字列か判定する
  * もし, ハッシュテーブルに格納された要素数がバケットサイズの70%を超えていたら, ハッシュテーブルを作り直す
  * keyのハッシュ値を取得し, 適切な位置にitemを保存する
* get(self, key)
  * キーに対応する値を取り出す関数
  * 対応するものがなければ(None, False)を返す
* delete(self, key)
  * 指定されたキーのitemを削除する関数
  * もし, ハッシュテーブルに格納された要素数がバケットサイズの30%を下回っていたら, ハッシュテーブルを作り直す
  * itemに連結するitemが存在しないとき, もしキーが探しているkeyならばそのバケットに含まれるデータをNoneにしてitemを削除, メモリ解放をする
  * itemに連結するitemが存在するとき, それが連結リストの先頭ならば隣接するitemを連結リストの先頭にしてitemを削除, メモリ解放をする
  * itemに連結するitemが存在するとき, それが連結リストの先頭でないならばitem.next.nextをitem.nextにしてitem.nextを削除, メモリ解放をする
* size(self)
  * ハッシュテーブルに含まれる要素数を返す
* check_size(self)
  * ハッシュテーブルのサイズが適切かを評価する

## 結果
実行結果をout.txtに記した. 実行結果はデータが増えても遅くならず, O(1)できちんと動くことができると確認できた.