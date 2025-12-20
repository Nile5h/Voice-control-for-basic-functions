def add(song, title):
    with open('songs.txt', 'a') as f:
        with open('songs.txt', 'r') as fs:
            lines = fs.readlines()
            for line in lines:
                s, t = line.strip().split(' ~ ')
                if s.lower() == song.lower():
                    return
        f.write(f"{song.lower()} ~ {title}\n")

def get(song):
    with open('songs.txt', 'r') as f:
        dict = {}
        for line in f:
            s, t = line.strip().split(' ~ ')
            dict[s] = t
        return dict.get(song.lower())

            