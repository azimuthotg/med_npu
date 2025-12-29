from django.core.management.base import BaseCommand
from apps.about.models import Department


class Command(BaseCommand):
    help = 'สร้างข้อมูลภาควิชาคณะแพทยศาสตร์ มหาวิทยาลัยนครพนม'

    def handle(self, *args, **kwargs):
        # ลบข้อมูลเก่าทั้งหมด (ถ้ามี)
        Department.objects.all().delete()
        self.stdout.write('ลบข้อมูลภาควิชาเก่าเรียบร้อย')

        # ภาควิชาพรีคลินิก (Pre-clinical Departments)
        preclinical_depts = [
            {
                'name': 'ภาควิชากายวิภาคศาสตร์',
                'name_en': 'Department of Anatomy',
                'description': 'ภาควิชาที่รับผิดชอบการเรียนการสอนด้านโครงสร้างของร่างกายมนุษย์',
                'order': 1
            },
            {
                'name': 'ภาควิชาจุลชีววิทยา',
                'name_en': 'Department of Microbiology',
                'description': 'ภาควิชาที่รับผิดชอบการเรียนการสอนด้านจุลินทรีย์และการติดเชื้อ',
                'order': 2
            },
            {
                'name': 'ภาควิชาปรสิตวิทยา',
                'name_en': 'Department of Parasitology',
                'description': 'ภาควิชาที่รับผิดชอบการเรียนการสอนด้านปรสิตและโรคที่เกี่ยวข้อง',
                'order': 3
            },
            {
                'name': 'ภาควิชาพยาธิคลินิก',
                'name_en': 'Department of Pathology',
                'description': 'ภาควิชาที่รับผิดชอบการเรียนการสอนด้านพยาธิวิทยาและการวินิจฉัยโรค',
                'order': 4
            },
            {
                'name': 'ภาควิชาชีวเคมีและพันธุวิศวกรรม',
                'name_en': 'Department of Biochemistry and Genetic Engineering',
                'description': 'ภาควิชาที่รับผิดชอบการเรียนการสอนด้านชีวเคมีและพันธุศาสตร์',
                'order': 5
            },
            {
                'name': 'ภาควิชาเภสัชวิทยา',
                'name_en': 'Department of Pharmacology',
                'description': 'ภาควิชาที่รับผิดชอบการเรียนการสอนด้านเภสัชวิทยาและยา',
                'order': 6
            },
        ]

        # ภาควิชาคลินิก (Clinical Departments)
        clinical_depts = [
            {
                'name': 'ภาควิชาอายุรศาสตร์',
                'name_en': 'Department of Internal Medicine',
                'description': 'ภาควิชาที่รับผิดชอบการรักษาโรคทางอายุรกรรม',
                'order': 7
            },
            {
                'name': 'ภาควิชาศัลยศาสตร์',
                'name_en': 'Department of Surgery',
                'description': 'ภาควิชาที่รับผิดชอบการผ่าตัดและการรักษาทางศัลยกรรม',
                'order': 8
            },
            {
                'name': 'ภาควิชาสูตินรีเวชศาสตร์',
                'name_en': 'Department of Obstetrics and Gynecology',
                'description': 'ภาควิชาที่รับผิดชอบการดูแลสุขภาพสตรีและการคลอด',
                'order': 9
            },
            {
                'name': 'ภาควิชากุมารเวชศาสตร์',
                'name_en': 'Department of Pediatrics',
                'description': 'ภาควิชาที่รับผิดชอบการดูแลสุขภาพเด็กและวัยรุ่น',
                'order': 10
            },
            {
                'name': 'ภาควิชาจิตเวชศาสตร์',
                'name_en': 'Department of Psychiatry',
                'description': 'ภาควิชาที่รับผิดชอบการรักษาโรคทางจิตเวช',
                'order': 11
            },
            {
                'name': 'ภาควิชาจักษุวิทยา',
                'name_en': 'Department of Ophthalmology',
                'description': 'ภาควิชาที่รับผิดชอบการรักษาโรคตาและการมองเห็น',
                'order': 12
            },
            {
                'name': 'ภาควิชานิติเวชศาสตร์',
                'name_en': 'Department of Forensic Medicine',
                'description': 'ภาควิชาที่รับผิดชอบการชันสูตรพลิกศพและนิติเวชศาสตร์',
                'order': 13
            },
            {
                'name': 'ภาควิชารังสีวิทยา',
                'name_en': 'Department of Radiology',
                'description': 'ภาควิชาที่รับผิดชอบการวินิจฉัยด้วยภาพรังสี',
                'order': 14
            },
            {
                'name': 'ภาควิชาวิสัญญีวิทยา',
                'name_en': 'Department of Anesthesiology',
                'description': 'ภาควิชาที่รับผิดชอบการดมยาสลบและการดูแลผู้ป่วยวิกฤต',
                'order': 15
            },
            {
                'name': 'ภาควิชาเวชศาสตร์ครอบครัว',
                'name_en': 'Department of Family Medicine',
                'description': 'ภาควิชาที่รับผิดชอบการดูแลสุขภาพแบบองค์รวมและเวชศาสตร์ครอบครัว',
                'order': 16
            },
            {
                'name': 'ภาควิชาเวชศาสตร์ชุมชน',
                'name_en': 'Department of Community Medicine',
                'description': 'ภาควิชาที่รับผิดชอบการสาธารณสุขชุมชนและเวชศาสตร์ป้องกัน',
                'order': 17
            },
            {
                'name': 'ภาควิชาเวชศาสตร์ฟื้นฟู',
                'name_en': 'Department of Rehabilitation Medicine',
                'description': 'ภาควิชาที่รับผิดชอบการฟื้นฟูสมรรถภาพผู้ป่วย',
                'order': 18
            },
            {
                'name': 'ภาควิชาเวชศาสตร์ฉุกเฉิน',
                'name_en': 'Department of Emergency Medicine',
                'description': 'ภาควิชาที่รับผิดชอบการดูแลผู้ป่วยฉุกเฉินและอุบัติเหตุ',
                'order': 19
            },
            {
                'name': 'ภาควิชาออร์โธปิดิคส์',
                'name_en': 'Department of Orthopedics',
                'description': 'ภาควิชาที่รับผิดชอบการรักษาโรคกระดูกและข้อ',
                'order': 20
            },
            {
                'name': 'ภาควิชาโสต นาสิก ลำคอ',
                'name_en': 'Department of Otolaryngology',
                'description': 'ภาควิชาที่รับผิดชอบการรักษาโรคหู คอ จมูก',
                'order': 21
            },
        ]

        # ภาควิชาการแพทย์แผนไทย (Thai Traditional Medicine)
        thai_medicine_dept = [
            {
                'name': 'ภาควิชาการแพทย์แผนไทย',
                'name_en': 'Department of Thai Traditional Medicine',
                'description': 'ภาควิชาที่รับผิดชอบการเรียนการสอนและการรักษาด้วยการแพทย์แผนไทย',
                'order': 22
            },
        ]

        # สร้างภาควิชาพรีคลินิก
        for dept_data in preclinical_depts:
            Department.objects.create(
                department_type='preclinical',
                is_active=True,
                **dept_data
            )
        self.stdout.write(self.style.SUCCESS(f'สร้างภาควิชาพรีคลินิก {len(preclinical_depts)} ภาควิชา'))

        # สร้างภาควิชาคลินิก
        for dept_data in clinical_depts:
            Department.objects.create(
                department_type='clinical',
                is_active=True,
                **dept_data
            )
        self.stdout.write(self.style.SUCCESS(f'สร้างภาควิชาคลินิก {len(clinical_depts)} ภาควิชา'))

        # สร้างภาควิชาการแพทย์แผนไทย
        for dept_data in thai_medicine_dept:
            Department.objects.create(
                department_type='thai_medicine',
                is_active=True,
                **dept_data
            )
        self.stdout.write(self.style.SUCCESS(f'สร้างภาควิชาการแพทย์แผนไทย {len(thai_medicine_dept)} ภาควิชา'))

        total = len(preclinical_depts) + len(clinical_depts) + len(thai_medicine_dept)
        self.stdout.write(self.style.SUCCESS(f'\n✅ สร้างข้อมูลภาควิชาทั้งหมด {total} ภาควิชาเรียบร้อย'))
