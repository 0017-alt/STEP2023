# Week7 mallocの実装

## best-fitについて
```
my_metadata_t *best_fit = NULL;
my_metadata_t *prev_best_fit = NULL;
my_metadata_t *metadata = my_head.free_head;
my_metadata_t *prev = NULL;

while (metadata) {
  if (metadata->size >= size && (!best_fit || metadata->size < best_fit->size)) {
    best_fit = metadata;
    prev_best_fit = prev;
  }
  prev = metadata;
  metadata = metadata->next;
}
```
my_malloc内に以上のような実装を行なった. これは, メタデータを全探索して, そのサイズがsizeより大きい, かつ現在のbest_fitのサイズよりも小さいという条件を満たすならばbest_fitを更新していくというアルゴリズムになっている.
結果はbest_fit.pngのようになった. 参考のため, first_bin.pngも見ると, Utilizationが明らかに向上していた.

## free_list_binについて
```
#define BIN_SIZE 5

size_t findNearestPowerOfTwo(size_t num) {
  size_t power = 0;
  while (1024 * power <= num) {
      power++;
  }
  return power - 1;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
  size_t bin_index = findNearestPowerOfTwo(metadata->size);
  if (prev) {
    prev->next = metadata->next;
  } else {
    bins[bin_index].free_head = metadata->next;
  }
  metadata->next = NULL;
}

void my_add_to_free_list(my_metadata_t *metadata) {
  assert(!metadata->next);
  size_t bin_index = findNearestPowerOfTwo(metadata->size);
  metadata->next = bins[bin_index].free_head;
  bins[bin_index].free_head = metadata;
}

void *my_malloc(size_t size) {
  my_metadata_t *best_fit = NULL;
  my_metadata_t *prev_best_fit = NULL;
  size_t bin_index = findNearestPowerOfTwo(size);
  for (size_t i = bin_index; i < BIN_SIZE; i++) {
    my_metadata_t *metadata = bins[i].free_head;
    my_metadata_t *prev = NULL;
    while (metadata) {
      if (metadata->size >= size && (!best_fit || metadata->size < best_fit->size)) {
        best_fit = metadata;
        prev_best_fit = prev;
      }
      prev = metadata;
      metadata = metadata->next;
    }
    if (best_fit) {
      break;
    }
  }
  .........
}
```
以上のように, bin_sizeは5とし, 1024で範囲を4等分することで行なった. best_fitを探索するときは, 対応するbin_index以上の値で探索し, best_fitが見つかった時点でループを抜けるようにした.
結果はfree_list_bin.pngのようになった. 速度は向上したが, Utilizationは明らかに悪くなったので, 領域の結合などをできたらより良くなりそうだと思った.