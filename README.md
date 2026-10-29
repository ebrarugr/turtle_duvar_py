# Duvardan Kaçan Kaplumbağa — ROS 2 Ödevi

Bu proje `turtle_duvar_py` adlı, Python (`rclpy`) ile yazılmış bir ROS 2 paketidir. Kaplumbağanın konumunu `/turtle1/pose` üzerinden dinler; `/turtle1/cmd_vel` üzerinden hareket komutu gönderir. Kaplumbağa **x veya y değeri 1.0'ın altına ya da 10.0'ın üstüne geldiğinde / sınıra ulaştığında**, duvardan yansıyacak şekilde yön değiştirir. Normal hareket sırasında ileri gider, dönerken durup kendi etrafında döner.

## Ödev maddeleri

1. **Paket:** `turtle_duvar_py`, `rclpy`, `geometry_msgs`, `turtlesim` kullanılır.
2. **Abone:** `turtlesim/msg/Pose` türündeki `/turtle1/pose` konusu; `x`, `y`, `theta` okunur.
3. **Yayıncı:** `geometry_msgs/msg/Twist` türündeki `/turtle1/cmd_vel` konusu; duvarda açı hesaplanıp yön değiştirilir.
4. **Log:** `get_logger().info()` ile konum **saniyede bir** yazdırılır.
5. **Bonus:** `hiz`, `alt_sinir`, `ust_sinir` parametreleri vardır.

## Gereksinimler

- Ubuntu üzerinde kurulmuş **ROS 2** (örn. Humble, Jazzy veya Kilted)
- `turtlesim` ve `python3-colcon-common-extensions`
- ROS 2 ortamının terminale yüklenmesi (`source /opt/ros/<dagitim>/setup.bash`)

> Aşağıdaki örnek ROS 2 **Jazzy** içindir. `jazzy` yerine sisteminizdeki dağıtımı yazın. Mevcut dağıtımları `ls /opt/ros` ile görebilirsiniz.

```bash
source /opt/ros/humble/setup.bash
sudo apt update
sudo apt install ros-$ROS_DISTRO-turtlesim python3-colcon-common-extensions
```

## Kurulum

İndirilen `turtle_duvar_py` klasörünü çalışma alanındaki `src` içine yerleştirin:

```bash
mkdir -p ~/ros2_ws/src
cp -r turtle_duvar_py ~/ros2_ws/src/
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select turtle_duvar_py
source install/setup.bash
```

> `cp -r` komutunu, `turtle_duvar_py` klasörünün bulunduğu dizinde çalıştırın. Eğer klasör zaten `~/ros2_ws/src` içindeyse kopyalamayın.

## Çalıştırma (tek terminal)

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch turtle_duvar_py turtle_duvar.launch.py
```

Bu komut **hem turtlesim penceresini hem de kontrol düğümünü** açar.

### Ayrı terminallerde çalıştırma

İlk terminal:

```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node
```

İkinci terminal:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run turtle_duvar_py duvar_kontrol
```

### Parametrelerle başlatma (bonus)

Kontrol düğümünü ayrı başlatırken varsayılan hızı ve sınırları değiştirebilirsiniz:

```bash
ros2 run turtle_duvar_py duvar_kontrol --ros-args \
  -p hiz:=1.5 -p alt_sinir:=1.5 -p ust_sinir:=9.5
```

Varsayılan parametreler: `hiz=2.0`, `alt_sinir=1.0`, `ust_sinir=10.0`. Sınırlar için `0 < alt_sinir < ust_sinir < 11` koşulu aranır. Bu parametreler düğüm başlarken okunur; değiştirmek için düğüm yeniden başlatılır.

## Sistem nasıl çalışır?

1. `/turtle1/pose` mesajından `x`, `y` ve `theta` alınır.
2. 0.05 saniyelik zamanlayıcı (20 Hz) hareket komutlarını günceller.
3. Konum sınıra geldiğinde kaplumbağanın gittiği yön duvarın dışını gösteriyorsa yansıma açısı hesaplanır.
   - Sağ veya sol duvar: `yeni_aci = pi - theta`
   - Üst veya alt duvar: `yeni_aci = -theta`
   - Köşede her iki kural sırayla uygulanır.
4. Kaplumbağa önce ileri hareketi durdurur, uygun açıya döner, ardından ileri gitmeye devam eder.
5. Bir saniyelik zamanlayıcı, konumu `logger.info` ile terminale yazar.

Yalnızca duvara doğru gidildiğinde dönüş başlatıldığı için, duvardan uzaklaşırken aynı duvara tekrar tekrar takılmaz.

### Terminalde görülecek log biçimi

Bunlar **örnek biçimdir**; gerçek değerler çalıştırma sırasında değişir.

```text
[INFO] [duvar_kontrol]: Duvar kontrol basladi. Hiz=2.0, sinirlar=[1.0, 10.0]
[INFO] [duvar_kontrol]: Konum: x=6.25, y=5.54, theta=0.00
[INFO] [duvar_kontrol]: Duvara yaklasildi! x=10.02, y=5.54; yon degistiriliyor.
[INFO] [duvar_kontrol]: Konum: x=9.86, y=5.54, theta=3.14
```

## Kod ve dosyalar

```text
turtle_duvar_py/
├── package.xml
├── setup.py
├── setup.cfg
├── README.md
├── .gitignore
├── resource/
│   └── turtle_duvar_py
├── turtle_duvar_py/
│   ├── __init__.py
│   ├── duvar_kontrol.py
│   └── hareket_mantigi.py
├── launch/
│   └── turtle_duvar.launch.py
├── test/
│   └── test_hareket_mantigi.py
└── ekran_goruntuleri/
    └── README.md
```

## Test

ROS 2 kurulumu gerektirmeyen hesaplama testleri:

```bash
cd ~/ros2_ws/src/turtle_duvar_py
python3 -m unittest discover -s test -v
```

Düğümlerin ROS 2 konularını doğru kullanıp kullanmadığını görmek için:

```bash
ros2 topic echo /turtle1/pose
ros2 topic info /turtle1/cmd_vel
```

## Ekran görüntüsü alma

Gerçek uygulamayı çalıştırdıktan sonra `ekran_goruntuleri/` içine en az şu üç görseli ekleyin:

1. `01_turtlesim_hareket.png`: turtlesim penceresinde hareket izi.
2. `02_terminal_log.png`: terminalde `Konum:` satırları.
3. `03_duvar_donusu.png`: terminalde `Duvara yaklasildi!` satırı ve dönüş.

Ubuntu'da `PrtSc` tuşuyla ekran görüntüsü alabilir, PNG dosyalarını bu klasöre taşıyabilirsiniz.

**Not:** Bu proje çalıştırılmamış bir ortamda oluşturuldu; gerçek ROS 2 ekran görüntüleri teslim paketine dahil değildir.

## GitHub üzerinden teslim

GitHub'da `turtle_duvar_py` adlı **boş** bir depo oluşturun (README ekleme seçeneğini kapatın). Ardından:

```bash
cd ~/ros2_ws/src/turtle_duvar_py
git init
git add .
git commit -m "ROS2 duvardan kacan kaplumbaga odevi"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADINIZ/turtle_duvar_py.git
git push -u origin main
```

`KULLANICI_ADINIZ` bölümünü kendi GitHub kullanıcı adınızla değiştirin. GitHub'a gönderirken **gerçek ekran görüntülerini de** `ekran_goruntuleri/` dizinine koyup commit edin. Ödev teslim alanına bu GitHub depo bağlantısını verin.
