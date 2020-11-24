# Maintainer: Andre Haehnel <andre.haehnel@t-online.de>
pkgname=update-nginx-mirrorlist
pkgver=1.1
pkgrel=1
pkgdesc="python script to create ngnix config snip in for nginx pacman proxy cache"
arch=('any')
license=('BSD')
depends=('nginx' 'python')
source=("update-nginx.py")
md5sums=('f95c0aa075ba86f4e5c51d31e9494585')

package() {
    install -Dm755 "$srcdir/update-nginx.py" "$pkgdir/usr/bin/mirrorlist-update-nginx"
}
