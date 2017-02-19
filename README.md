# mmap_batcher

In training machine learning models, it is sometimes necessary to access large files, which may not fit into memory. To further complicate matters, it is generally the case each epoch of training receives a shuffled representation of the data. This class facilitates a number of different features in this regard. 

 * filename: file name
 * batch_size: size of each batch where the batch is a set of lines in the file; default 100
 * shuffle: boolean to shuffle batched records; default True
 * ignore_leftovers: boolean to ignore leftover lines at the end of the epoch; default True
 * skip_blank_lines: boolean; default True
 * comment_char: skip lines starting with this character; default '#'
 * number of epochs may be set in the epochs method
 
Under the covers, this uses a memory mapped file and file byte offsets (to the beginning of each line) are stored internally. These offsets are shuffled in order to randomize access to the file. 
 
A common use case is below. 

```
mmb = MmapBatcher('/tmp/numbers.txt', batch_size=3)
for epoch in mmb.epochs(2):
    for b in epoch.batches():
        print(b)
    print('-----------------')
    
# output
# [b'nine nine nine nine nine nine nine nine nine\n', b'five five five five five\n', b'eight eight eight eight eight eight eight eight\n']
# [b'three three three\n', b'six six six six six six\n', b'one\n']
# [b'two two\n', b'four four four four\n', b'seven seven seven seven seven seven seven\n']
# -----------------
# [b'seven seven seven seven seven seven seven\n', b'eight eight eight eight eight eight eight eight\n', b'five five five five five\n']
# [b'four four four four\n', b'two two\n', b'six six six six six six\n']
# [b'three three three\n', b'nine nine nine nine nine nine nine nine nine\n', b'one\n']
# -----------------
```
Input file
```
# comment
one
two two
three three three
    
four four four four
five five five five five 
six six six six six six 
seven seven seven seven seven seven seven 
eight eight eight eight eight eight eight eight 
nine nine nine nine nine nine nine nine nine 
ten ten ten ten ten ten ten ten ten ten 
```
