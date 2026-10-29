"""ROS 2 turtlesim: sınırda yön değiştiren kaplumbağa."""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from turtle_duvar_py.hareket_mantigi import aciyi_normalize_et, yeni_yon_hesapla


class DuvarKontrol(Node):
    def __init__(self):
        super().__init__('duvar_kontrol')

        # Bonus: hız ve duvar sınırları ROS 2 parametreleridir.
        self.declare_parameter('hiz', 2.0)
        self.declare_parameter('alt_sinir', 1.0)
        self.declare_parameter('ust_sinir', 10.0)

        self.hiz = float(self.get_parameter('hiz').value)
        self.alt_sinir = float(self.get_parameter('alt_sinir').value)
        self.ust_sinir = float(self.get_parameter('ust_sinir').value)

        if self.hiz <= 0.0:
            raise ValueError('hiz parametresi 0\'dan büyük olmalıdır.')
        if not 0.0 < self.alt_sinir < self.ust_sinir < 11.0:
            raise ValueError('Sınırlar 0 < alt_sinir < ust_sinir < 11 olmalıdır.')

        self.konum = None
        self.donus_hedefi = None

        # Abone: turtlesim'den x, y ve yön (theta) bilgileri gelir.
        self.pose_abonesi = self.create_subscription(
            Pose, '/turtle1/pose', self.konumu_al, 10
        )

        # Yayıncı: kaplumbağaya hız ve dönüş komutu gönderir.
        self.hiz_yayincisi = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )

        # 20 Hz hareket kontrolü; saniyede bir log.
        self.create_timer(0.05, self.hareket_et)
        self.create_timer(1.0, self.konumu_yazdir)

        self.get_logger().info(
            f'Duvar kontrol basladi. Hiz={self.hiz:.1f}, '
            f'sinirlar=[{self.alt_sinir:.1f}, {self.ust_sinir:.1f}]'
        )

    def konumu_al(self, mesaj):
        self.konum = mesaj

    def hareket_et(self):
        if self.konum is None:
            return

        komut = Twist()

        if self.donus_hedefi is None:
            self.donus_hedefi = yeni_yon_hesapla(
                self.konum.x,
                self.konum.y,
                self.konum.theta,
                self.alt_sinir,
                self.ust_sinir,
            )
            if self.donus_hedefi is not None:
                self.get_logger().info(
                    f'Duvara yaklasildi! x={self.konum.x:.2f}, '
                    f'y={self.konum.y:.2f}; yon degistiriliyor.'
                )

        if self.donus_hedefi is not None:
            hata = aciyi_normalize_et(
                self.donus_hedefi - self.konum.theta
            )
            if abs(hata) > 0.03:
                # Önce yerinde dön, ardından ileri git.
                komut.linear.x = 0.0
                komut.angular.z = max(-2.5, min(2.5, 5.0 * hata))
                self.hiz_yayincisi.publish(komut)
                return
            self.donus_hedefi = None

        komut.linear.x = self.hiz
        komut.angular.z = 0.0
        self.hiz_yayincisi.publish(komut)

    def konumu_yazdir(self):
        if self.konum is not None:
            self.get_logger().info(
                f'Konum: x={self.konum.x:.2f}, '
                f'y={self.konum.y:.2f}, '
                f'theta={self.konum.theta:.2f}'
            )

    def durdur(self):
        self.hiz_yayincisi.publish(Twist())


def main(args=None):
    rclpy.init(args=args)
    kontrol = None
    try:
        kontrol = DuvarKontrol()
        rclpy.spin(kontrol)
    except KeyboardInterrupt:
        pass
    finally:
        if kontrol is not None:
            kontrol.durdur()
            kontrol.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
