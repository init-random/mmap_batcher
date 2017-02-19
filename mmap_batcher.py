import mmap
import re


class MmapBatcher:
    
    def __init__(self, filename, batch_size=100, shuffle=True, ignore_leftovers=True,
                 skip_blank_lines=True, comment_char='#'):
        self.filename = filename
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.ignore_leftovers = ignore_leftovers
        self.skip_blank_lines = skip_blank_lines
        self.comment_char = comment_char
        self.offsets = None
        
    def batches(self):
        if self.offsets is None:
            self._get_offsets()
            
        if self.shuffle is True:
            np.random.shuffle(self.offsets)

        with open(self.filename, 'r') as f:
            mm = mmap.mmap(f.fileno(), 0, access = mmap.ACCESS_READ)   
            
            # start/end index
            s_idx = 0
            e_idx = self.batch_size
            while s_idx<=len(self.offsets):
                _offsets = self.offsets[s_idx:e_idx]
                if self.ignore_leftovers and len(_offsets)<self.batch_size: break
                s_idx += self.batch_size
                e_idx += self.batch_size
                lines = []
                for _offset in _offsets:
                    mm.seek(_offset)
                    lines.append(mm.readline())
                yield lines
                
    def epochs(self, n_epochs):
        for epoch in range(n_epochs):
            yield self
        
    
    def _get_offsets(self):
        offsets = []
        prev_loc = 0
        with open(self.filename, 'r') as f:
            mm = mmap.mmap(f.fileno(), 0, access = mmap.ACCESS_READ) 
            f_sz = mm.size()
            while True:
                l = mm.readline()
                loc = mm.tell()  
                if loc>=f_sz: break
                blank_line = False
                if self.skip_blank_lines and re.match('^\s*$', l.decode('utf8')) is not None:
                    blank_line = True
                if not l.decode('utf8').startswith(self.comment_char) and not blank_line:
                    offsets.append(prev_loc) 
                prev_loc = loc

        self.offsets = offsets
