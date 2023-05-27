# 第3週課題
## 宿題1 「*」「/」への対応
* 「*」や「/」を読んだら, man_mul/man_div関数へ移行する
* man_mul/man_div関数では, tokensの1つ前の数値をtokensからpopするとともに, 後続する数値を計算する
* もし「*」「/」の直後が「(」ならば, 「)」が来るまでtokensを計算してその結果を取得する
* もし「*」「/」の直後が数値ならば, read_numberをしてその数値を取得する
* tokensに取得した2つの数値の計算結果をNUMBERとして登録する
* その後, PLUS, MINUSのみのtokens列をevaluateして値を求める

## 宿題3 括弧への対応
* 「(」を読み取ったら, man_bracket関数へ移行
* man_bracket関数では, 後続のlineを「)」まで読んでその値をevaluateし, NUMBERとしてtokensに登録する
* indexは「()」の中身の分だけ増やしておく
* 括弧の中に括弧が来ても再帰関数をスタック状に呼び出しているので, 対応ができる