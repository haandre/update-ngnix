# Maintainer: Andre Haehnel <andre.haehnel@t-online.de>
pkgname=update-nginx-mirrorlist
pkgver=1.0
pkgrel=1
pkgdesc="python script to create ngnix config snip in for nginx pacman proxy cache"
arch=('any')
license=('BSD')
depends=('nginx' 'python')
source=("update-nginx.py")
md5sums=('f0fadd17a852f922b3ffaff678f3a78e')

package() {
    install -Dm755 "$srcdir/update-nginx.py" "$pkgdir/usr/bin/mirrorlist-update-nginx"
}
