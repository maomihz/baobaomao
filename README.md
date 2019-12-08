# CoreDNS

* GitHub: https://github.com/coredns/coredns
* Version: v1.6.5

```
docker run -it --rm -v $PWD:/app golang bash
```

```
cd /app
GOOS=linux GOARCH=386 go build -v -o coredns-v1.6.5-linux-386
GOOS=linux GOARCH=amd64 go build -v -o coredns-v1.6.5-linux-amd64
```

# Tmux

* GitHub: https://github.com/tmux/tmux.git
* Release: https://github.com/tmux/tmux/releases/download/3.0a/tmux-3.0a.tar.gz
* Version: v3.0a
* Dependencies:
  * libevent (alpine)
  * ncurses (alpine)

```
tar xzf tmux-3.0a.tar.gz
cd tmux-3.0a
docker run -it --rm -v $PWD:/app maomihz/alpine-build bash
apk add libevent-dev libevent-static ncurses-dev ncurses-static
```

```
cd /app
./configure --enable-static
make
strip tmux
```

```
$ ldd tmux
        /lib/ld-musl-x86_64.so.1 (0x7f1af3efe000)
$ ./tmux -V
tmux 3.0a
```

# Xmrig

* Github: https://github.com/xmrig/xmrig
* Version: 5.1.1
* Dependencies:
  * libuv **v1.34.0** https://dist.libuv.org/dist/v1.34.0/libuv-v1.34.0.tar.gz
  * hwloc **v2.0.4** https://download.open-mpi.org/release/hwloc/v2.0/hwloc-2.0.4.tar.gz
  * openssl **1.1.1d** https://www.openssl.org/source/openssl-1.1.1d.tar.gz
  * libmicrohttpd **0.9.63** https://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-0.9.63.tar.gz

```
tar xzf hwloc-2.0.4.tar.gz
tar xzf libmicrohttpd-0.9.63.tar.gz
tar xzf libuv-v1.34.0.tar.gz
tar xzf openssl-1.1.1d.tar.gz

docker run -it --rm -v $PWD:/app maomihz/alpine-build
```

```
cd /app/openssl-1.1.1d
./config no-shared --prefix=/app/prefix
make -j 8
make install
```

```
cd /app/libuv-v1.34.0
./autogen.sh
./configure --disable-shared --prefix=/app/prefix
make -j 8
make install
```

```
cd /app/hwloc-2.0.4
./configure --disable-shared --prefix=/app/prefix
make -j 8
make install
```

```
cd /app/libmicrohttpd-0.9.63
./configure --disable-shared --prefix=/app/prefix
make -j 8
make install
```

```
cd /app
mkdir build
cd build

cmake .. -DBUILD_STATIC=ON -DCMAKE_PREFIX_PATH=/app/prefix
make -j 8
```

```
$ ldd xmrig
        /lib/ld-musl-x86_64.so.1 (0x7f6e6f4d8000)
$ ./xmrig -V
XMRig 5.1.1
 built on Dec  8 2019 with GCC 8.3.0
 features: 64-bit AES

libuv/1.34.0
OpenSSL/1.1.1d
hwloc/2.0.4
```
