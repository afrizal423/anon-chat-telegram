# Kumpulan catatan pada bot ini

### Menyalakan redis
```bash
sudo service redis-server stop
redis-server redis.conf
```

## Command
- start
- cari_partner
- lewati
- berhenti
- about
https://telegra.ph/Tentang-FindPartnerChat-10-13
- rules
bangun pagi pergi membajak...
membajak sawah di tepi jalan...
bila kamu orang yang bijak...
maka taatlah pada peraturan...
atau
buah siksak
buah durian
jika kamu bijak
turuti peraturan
https://telegra.ph/Peraturan-Chat-di-FindPartnerChat-10-13
- donasi
- bantuan
Bocah ganteng namanya Gopal
Tetap bekerja meski anak konglomerat
Bolehkah kiranya kita saling kenal?
Perkenalkan nama saya FindPartnerChat

Cari tempat tak kunjung dapat
Ternyata alamatnya dekat surau
Perkenalkan nama saya FindPartnerChat
Tempatnya orang bersenda gurau

```sql
select id_user, username_user, firstname_user, jeniskelamin_user, ketertarikan_user, (
select status from tbl_iddle where id_user = tbl_pengguna.id_user) as statusnya
from tbl_pengguna
where ( id_user in (
select id_user from tbl_iddle
where status = 'true') and
jeniskelamin_user = 'L' and
id_user != '576507972') or (
id_user in (
select id_user from tbl_iddle
where status = 'true') and
jeniskelamin_user = 'P' and
id_user != '576507972') 
```