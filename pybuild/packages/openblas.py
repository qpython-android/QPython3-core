from ..source import GitSource
from ..package import Package
from ..patch import LocalPatch
from ..util import target_arch

class OpenBLAS(Package):
    source = GitSource('https://github.com/AIPYX/OpenBLAS.git', alias='openblas', branch='qpyc/0.2.21')
    patches = [
        #LocalPatch('0001-set-stderr'),
    ]

    skip_uploading = True
    re_configure = True

    def prepare(self):
        pass

    def build(self):
        self.system(
            f'make PREFIX={self.destdir()}/usr ARM_SOFTFP_ABI=1 TARGET=ARMV7 HOSTCC=gcc CC=arm-linux-androideabi-gcc FC=arm-linux-androideabi-gfortran FFLAGS=\"--sysroot {self.env["ARCH_SYSROOT"]}/..\" CFLAGS=\"--sysroot {self.env["ARCH_SYSROOT"]}/..\" LDFLAGS=\"-L{self.env["ARCH_SYSROOT"]}/lib -L{self.env["ANDROID_NDK"]}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/arm-linux-androideabi/lib/armv7-a\" NETLIB_LAPACK_DIR=lapack-netlib'
            )
        self.run_with_env(['make', 'install', f'PREFIX={self.destdir()}/usr'])
        self.system(
            f'rm {self.destdir()}/usr/lib*so*'
        )
