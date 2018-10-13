# Ext Super Magic
**Category:** Forensics
>  We salvaged a ruined Ext SuperMagic II-class mech recently and pulled the
>  [filesystem](https://2018shell1.picoctf.com/static/9f563e291d847c30879277c3b6c16260/ext-super-magic.img)
>  out of the black box. It looks a bit corrupted, but maybe there's something
>  interesting in there. You can also find it in
>  /problems/ext-super-magic\_2\_5e1f8bfb15060228f577045924e4fca8 on the shell
>  server.
>
> Hints:
> - Are there any [tools](https://en.wikipedia.org/wiki/Fsck) for diagnosing
>   corrupted filesystems? What do they say if you run them on this one?
> - How does a linux machine know what
>   [type](https://www.garykessler.net/library/file_sigs.html) of file a
>   [file](https://linux.die.net/man/1/file) is?
> - You might find this [doc](http://www.nongnu.org/ext2-doc/ext2.html) helpful.
> - Be careful with [endianess](https://en.wikipedia.org/wiki/Endianness) when
>   making edits.
> - Once you've fixed the corruption, you can use
>   /sbin/[debugfs](https://linux.die.net/man/8/debugfs) to pull the flag file
>   out.

We're given a file containing a filesystem. Let's try running fsck, as in the
hints.

	$ fsck.ext2 ext-super-magic.img
	e2fsck 1.43.4 (31-Jan-2017)
	ext2fs_open2: Bad magic number in super-block
	fsck.ext2: Superblock invalid, trying backup blocks...
	fsck.ext2: Bad magic number in super-block while trying to open ext-super-magic.img
	[...]

It tells us that the magic number is wrong, so let's fix it! We're also given a
link to the ext2 documentation. A quick search for "magic" lands us in
`s_magic`, which is at offset 1024+56, with the value `0xEF53` (or
`EXT2_SUPER_MAGIC`). We just set this value, and we'll have a good filesystem.

```python
import struct

with open('ext-super-magic.img', 'rb') as f:
    fs = bytearray(f.read())

magic = 0xEF53
offset = 1024+56

fs[offset:offset+2] = struct.pack('<H', magic)

with open('fixed.img', 'wb') as f:
    f.write(fs)
```

Check if we did it right:

	$ fsck.ext2 fixed.img 
	e2fsck 1.43.4 (31-Jan-2017)
	fixed.img: clean, 512/1280 files, 3745/5120 blocks

Now, we can either mount it if we're working on a local environment or use
debugfs as recommended. Since here we're working on a local machine, we simply
`mount fixed.img /mnt`, read the file `flag.jpg` and obtain the flag.

flag: `picoCTF{ab0CD63BC762514ea2f4fc9eDEC8cb1E}`
