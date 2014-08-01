set -e
cd ~/src/ffmpeg_sources
curl -O http://www.tortall.net/projects/yasm/releases/yasm-1.2.0.tar.gz
tar xzvf yasm-1.2.0.tar.gz
cd yasm-1.2.0
./configure --prefix="$HOME" --bindir="$HOME/bin"
make
make install
make distclean

cd ~/src/ffmpeg_sources
git clone --depth 1 git://git.videolan.org/x264
cd x264
./configure --prefix="$HOME" --bindir="$HOME/bin" --enable-static
make
make install
make distclean

cd ~/src/ffmpeg_sources
git clone --depth 1 git://github.com/mstorsjo/fdk-aac.git
cd fdk-aac
autoreconf -fiv
./configure --prefix="$HOME" --disable-shared
make
make install
make distclean

cd ~/src/ffmpeg_sources
curl -L -O http://downloads.sourceforge.net/project/lame/lame/3.99/lame-3.99.5.tar.gz
tar xzvf lame-3.99.5.tar.gz
cd lame-3.99.5
./configure --prefix="$HOME" --bindir="$HOME/bin" --disable-shared --enable-nasm
make
make install
make distclean

cd ~/src/ffmpeg_sources
curl -O http://downloads.xiph.org/releases/opus/opus-1.0.3.tar.gz
tar xzvf opus-1.0.3.tar.gz
cd opus-1.0.3
./configure --prefix="$HOME" --disable-shared
make
make install
make distclean

cd ~/src/ffmpeg_sources
curl -O http://downloads.xiph.org/releases/ogg/libogg-1.3.1.tar.gz
tar xzvf libogg-1.3.1.tar.gz
cd libogg-1.3.1
./configure --prefix="$HOME" --disable-shared
make
make install
make distclean

cd ~/src/ffmpeg_sources
curl -O http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.3.tar.gz
tar xzvf libvorbis-1.3.3.tar.gz
cd libvorbis-1.3.3
./configure --prefix="$HOME" --with-ogg="$HOME" --disable-shared
make
make install
make distclean

cd ~/src/ffmpeg_sources
git clone --depth 1 http://git.chromium.org/webm/libvpx.git
cd libvpx
./configure --prefix="$HOME" --disable-examples
make
make install
make clean

cd ~/src/ffmpeg_sources
git clone --depth 1 git://source.ffmpeg.org/ffmpeg
cd ffmpeg
PKG_CONFIG_PATH="$HOME/lib/pkgconfig"
export PKG_CONFIG_PATH
./configure --prefix="$HOME" --extra-cflags="-I$HOME/include" --extra-ldflags="-L$HOME/lib" --bindir="$HOME/bin" --extra-libs="-ldl" --enable-gpl --enable-nonfree --enable-libfdk_aac --enable-libmp3lame --enable-libopus --enable-libvorbis --enable-libvpx --enable-libx264
make
make install
make distclean
#hash -r
