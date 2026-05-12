import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from products.models import Medicament

class Command(BaseCommand):
    help = 'Add realistic medications to the database (default target: 1284).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1284,
            help='Target number of medications to ensure in DB (only inserts missing ones).',
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            default=True,
            help='If a medicament with the same name exists, do not insert it again.',
        )

    def handle(self, *args, **kwargs):
        # Prix d'achat en Dirhams Marocains (MAD) par catégorie
        # Fourchettes réalistes pour le marché pharmaceutique marocain
        CATEGORY_PRICE_RANGES = {
            'Antalgique': (8, 25),
            'Antibiotique': (20, 80),
            'Anti-inflammatoire': (15, 60),
            'Antihistaminique': (12, 35),
            'Respiratoire': (15, 45),
            'Digestif': (15, 70),
            'Vitamine': (10, 40),
            'Cardiovasculaire': (30, 150),
            'Endocrinologie': (80, 250),
            'Antiparasitaire': (30, 120),
            'Dermatologie': (12, 50),
            'Ophtalmologie': (25, 70),
            'Neurologique': (20, 90),
            'Antiseptique': (5, 25),
        }

        medicament_data = [
            ('Amoxicilline 500mg', 'Antibiotique à large spectre pour infections bactériennes', 'Antibiotique'),
            ('Ibuprofène 400mg', 'Anti-inflammatoire non stéroïdien', 'Anti-inflammatoire'),
            ('Paracétamol 500mg', 'Antalgique et antipyrétique', 'Antalgique'),
            ('Céfuroxime 250mg', 'Céphalosporine de deuxième génération', 'Antibiotique'),
            ('Azithromycine 250mg', 'Macrolide pour infections respiratoires', 'Antibiotique'),
            ('Loratadine 10mg', 'Antihistaminique non sédatif', 'Antihistaminique'),
            ('Cétirizine 10mg', 'Antihistaminique pour allergies saisonnières', 'Antihistaminique'),
            ('Dextrométhorphane', 'Antitussif pour la toux sèche', 'Respiratoire'),
            ('Ambroxol 30mg', 'Mucolytique pour la toux grasse', 'Respiratoire'),
            ('Salbutamol 100mcg', 'Bronchodilatateur pour asthme', 'Respiratoire'),
            ('Oméprazole 20mg', 'Inhibiteur de la pompe à protons', 'Digestif'),
            ('Pantoprazole 40mg', 'Inhibiteur de la pompe à protons', 'Digestif'),
            ('Dompéridone 10mg', 'Prokinétique pour nausées et vomissements', 'Digestif'),
            ('Métronidazole 500mg', 'Antibiotique et antiparasitaire', 'Antibiotique'),
            ('Ciprofloxacine 500mg', 'Fluoroquinolone pour infections urinaires', 'Antibiotique'),
            ('Diclofénac 50mg', 'Anti-inflammatoire pour douleurs articulaires', 'Anti-inflammatoire'),
            ('Naproxène 250mg', 'AINS pour douleurs musculaires', 'Anti-inflammatoire'),
            ('Tramadol 50mg', 'Opioïde modéré pour douleurs intenses', 'Antalgique'),
            ('Codéine 30mg', 'Antalgique opioïde', 'Antalgique'),
            ('Morphine 10mg', 'Antalgique opioïde majeur', 'Antalgique'),
            ('Aspirine 500mg', 'Antalgique, antipyrétique et anti-inflammatoire', 'Anti-inflammatoire'),
            ('Vitamine C 500mg', 'Complément alimentaire antioxydant', 'Vitamine'),
            ('Vitamine D3 1000 UI', 'Complément pour la santé osseuse', 'Vitamine'),
            ('Vitamine B12', 'Complément pour le système nerveux', 'Vitamine'),
            ('Fer 100mg', 'Complément pour anémie ferriprive', 'Vitamine'),
            ('Magnésium 300mg', 'Complément pour fatigue et crampes', 'Vitamine'),
            ('Zinc 15mg', 'Complément pour immunité', 'Vitamine'),
            ('Calcium 500mg', 'Complément pour santé osseuse', 'Vitamine'),
            ('Amlodipine 5mg', 'Calcium antagoniste pour hypertension', 'Cardiovasculaire'),
            ('Lisinopril 10mg', 'IEC pour hypertension artérielle', 'Cardiovasculaire'),
            ('Valsartan 80mg', 'ARA II pour hypertension', 'Cardiovasculaire'),
            ('Métroprolol 50mg', 'Bêtabloquant pour hypertension', 'Cardiovasculaire'),
            ('Atorvastatine 20mg', 'Hypolipémiant statine', 'Cardiovasculaire'),
            ('Simvastatine 20mg', 'Statine pour cholestérol', 'Cardiovasculaire'),
            ('Acide acétylsalicylique 75mg', 'Antiagrégant plaquettaire', 'Cardiovasculaire'),
            ('Clopidogrel 75mg', 'Antiagrégant plaquettaire', 'Cardiovasculaire'),
            ('Warfarine 5mg', 'Anticoagulant oral', 'Cardiovasculaire'),
            ('Héparine', 'Anticoagulant injectable', 'Cardiovasculaire'),
            ('Insuline rapide', 'Insuline pour diabète de type 1 et 2', 'Endocrinologie'),
            ('Insuline lente', 'Insuline basale pour diabète', 'Endocrinologie'),
            ('Métformine 500mg', 'Antidiabétique oral biguanide', 'Endocrinologie'),
            ('Glibenclamide 5mg', 'Sulfamidé hypoglycémiant', 'Endocrinologie'),
            ('Glipizide 5mg', 'Sulfamidé hypoglycémiant', 'Endocrinologie'),
            ('Levothyroxine 50mcg', 'Hormone thyroïdienne de substitution', 'Endocrinologie'),
            ('Prednisone 20mg', 'Corticoïde systémique', 'Endocrinologie'),
            ('Hydrocortisone', 'Corticoïde pour insuffisance surrénale', 'Endocrinologie'),
            ('Fluconazole 150mg', 'Antifongique azolé', 'Antiparasitaire'),
            ('Itraconazole 100mg', 'Antifongique triazolé', 'Antiparasitaire'),
            ('Mébendazole 100mg', 'Antiparasitaire pour vers intestinaux', 'Antiparasitaire'),
            ('Albendazole 400mg', 'Antiparasitaire large spectre', 'Antiparasitaire'),
            ('Chloroquine 250mg', 'Antipaludique', 'Antiparasitaire'),
            ('Artéméther 20mg', 'Antipaludique de combinaison', 'Antiparasitaire'),
            ('Luméfantrine 120mg', 'Antipaludique associé', 'Antiparasitaire'),
            ('Bêtaméthasone', 'Corticoïde topique puissant', 'Dermatologie'),
            ('Hydrocortisone 1%', 'Corticoïde topique léger', 'Dermatologie'),
            ('Miconazole 2%', 'Antifongique topique', 'Dermatologie'),
            ('Clotrimazole 1%', 'Antifongique topique', 'Dermatologie'),
            ('Kétoconazole', 'Antifongique topique et systémique', 'Dermatologie'),
            ('Aciclovir 5%', 'Antiviral topique pour herpès', 'Dermatologie'),
            ('Benzoyle peroxyde', 'Antiacnéique topique', 'Dermatologie'),
            ('Rétinoïde', 'Dérivé de vitamine A pour acné', 'Dermatologie'),
            ('Gentamicine', 'Antibiotique topique aminoglycoside', 'Dermatologie'),
            ('Chloramphénicol 1%', 'Antibiotique topique large spectre', 'Ophtalmologie'),
            ('Tobramycine', 'Antibiotique ophtalmique aminoglycoside', 'Ophtalmologie'),
            ('Ciprofloxacine collyre', 'Antibiotique ophtalmique fluoroquinolone', 'Ophtalmologie'),
            ('Dexaméthasone collyre', 'Corticoïde ophtalmique', 'Ophtalmologie'),
            ('Pilocarpine', 'Parasympathomimétique pour glaucome', 'Ophtalmologie'),
            ('Timolol 0.5%', 'Bêtabloquant ophtalmique pour glaucome', 'Ophtalmologie'),
            ('Diazepam 10mg', 'Anxiolytique benzodiazépine', 'Neurologique'),
            ('Alprazolam 0.5mg', 'Anxiolytique pour crises d\'angoisse', 'Neurologique'),
            ('Lorazepam 2mg', 'Anxiolytique court terme', 'Neurologique'),
            ('Amitriptyline 25mg', 'Antidépresseur tricyclique', 'Neurologique'),
            ('Sertraline 50mg', 'Antidépresseur ISRS', 'Neurologique'),
            ('Fluoxétine 20mg', 'Antidépresseur ISRS', 'Neurologique'),
            ('Carbamazépine 200mg', 'Antiepileptique stabilisateur', 'Neurologique'),
            ('Valproate 500mg', 'Antiepileptique et thymorégulateur', 'Neurologique'),
            ('Lévétiracétam 500mg', 'Antiepileptique de nouvelle génération', 'Neurologique'),
            ('Lamotrigine 25mg', 'Antiepileptique stabilisateur', 'Neurologique'),
            ('Povidone iodée 10%', 'Antiseptique cutané', 'Antiseptique'),
            ('Chlorhexidine 0.05%', 'Antiseptique pour lavage des mains', 'Antiseptique'),
            ('Alcool isopropylique 70%', 'Antiseptique pour désinfection', 'Antiseptique'),
            ('Eau oxygénée 10 volumes', 'Antiseptique et désinfectant', 'Antiseptique'),
            ('Permanganate de potassium', 'Antiseptique et antifongique', 'Antiseptique'),
            ('Phénobarbital 100mg', 'Antiepileptique et sédatif', 'Neurologique'),
            ('Phénytoïne 100mg', 'Antiepileptique hydantoïne', 'Neurologique'),
            ('Gabapentine 300mg', 'Antiepileptique et antalgique neuropathique', 'Neurologique'),
            ('Pregabaline 75mg', 'Antalgique neuropathique', 'Neurologique'),
            ('Sumatriptan 50mg', 'Antimigraineux triptan', 'Neurologique'),
            ('Rizatriptan 10mg', 'Antimigraineux triptan', 'Neurologique'),
            ('Propranolol 40mg', 'Bêtabloquant pour prophylaxie migraine', 'Neurologique'),
            ('Nitroglycérine 0.4mg', 'Antiangoreux sous-lingual', 'Cardiovasculaire'),
            ('Isosorbide mononitrate', 'Antiangoreux de longue durée', 'Cardiovasculaire'),
            ('Digoxine 0.25mg', 'Cardiotonique pour insuffisance cardiaque', 'Cardiovasculaire'),
            ('Furosémide 40mg', 'Diurétique de l\'anse pour œdèmes', 'Cardiovasculaire'),
            ('Spironolactone 25mg', 'Diurétique antagoniste de l\'aldostérone', 'Cardiovasculaire'),
            ('Hydrochlorothiazide', 'Diurétique thiazidique', 'Cardiovasculaire'),
            ('Ranitidine 150mg', 'Antihistaminique H2 pour ulcère', 'Digestif'),
            ('Lansoprazole 30mg', 'Inhibiteur de la pompe à protons', 'Digestif'),
            ('Esomeprazole 40mg', 'Inhibiteur de la pompe à protons', 'Digestif'),
            ('Sucralfate 1g', 'Protecteur gastrique', 'Digestif'),
            ('Lactulose', 'Laxatif osmotique', 'Digestif'),
            ('Séné', 'Laxatif stimulant', 'Digestif'),
            ('Bisacodyl 5mg', 'Laxatif stimulant', 'Digestif'),
            ('Ondansétron 4mg', 'Antiemétique anti-5HT3', 'Digestif'),
            ('Métopimazine', 'Antiemétique neuroleptique', 'Digestif'),
            ('Lopéramide 2mg', 'Antidiarrhéique opioïde', 'Digestif'),
            ('Racecadotril', 'Antisécrétoire intestinal', 'Digestif'),
            ('Aciclovir 200mg', 'Antiviral systémique pour herpès et zona', 'Antiparasitaire'),
            ('Valaciclovir 500mg', 'Prodrug de l\'aciclovir', 'Antiparasitaire'),
            ('Oseltamivir 75mg', 'Antiviral pour grippe A et B', 'Antiparasitaire'),
            ('Zanamivir', 'Antiviral pour grippe par inhalation', 'Antiparasitaire'),
            ('Ribavirine', 'Antiviral pour infections chroniques', 'Antiparasitaire'),
            ('Méthotrexate 2.5mg', 'Immunosuppresseur et chimiothérapie', 'Anti-inflammatoire'),
            ('Azathioprine 50mg', 'Immunosuppresseur', 'Anti-inflammatoire'),
            ('Ciclosporine', 'Immunosuppresseur anti-rejet', 'Anti-inflammatoire'),
            ('Colchicine 0.5mg', 'Traitement de la goutte', 'Anti-inflammatoire'),
            ('Allopurinol 100mg', 'Hypouricémiant préventif goutte', 'Anti-inflammatoire'),
            ('Febuxostat 80mg', 'Hypouricémiant de nouvelle génération', 'Anti-inflammatoire'),
        ]

        count = int(kwargs.get('count') or 1284)
        skip_existing = bool(kwargs.get('skip_existing', True))

        random.seed(42)

        # on part des données de base, puis on génère des variantes si on a besoin de plus
        base_len = len(medicament_data)
        created = 0
        idx = 0

        while created < count:
            idx += 1
            base_index = (idx - 1) % base_len
            base_nom, base_description, base_categorie = medicament_data[base_index]

            # Générer un nom unique/variant pour éviter les doublons de base.
            # Exemple: "Paracétamol 500mg" -> "Paracétamol 500mg (Lot 17)"
            nom = base_nom if idx <= base_len else f"{base_nom} (Lot {idx - base_len})"

            if skip_existing and Medicament.objects.filter(nom=nom).exists():
                continue

            prix_min, prix_max = CATEGORY_PRICE_RANGES.get(base_categorie, (10, 50))
            prix_achat = round(random.uniform(prix_min, prix_max), 2)
            prix_vente = round(prix_achat * random.uniform(1.20, 1.30), 2)
            date_expiration = datetime.now().date() + timedelta(days=random.randint(180, 1825))
            quantite_stock = random.randint(5, 500)

            description = base_description
            if idx > base_len:
                description = f"{base_description} (variante #{idx - base_len})"

            Medicament.objects.create(
                nom=nom,
                description=description,
                prix_achat=prix_achat,
                prix_vente=prix_vente,
                date_expiration=date_expiration,
                categorie=base_categorie,
                quantite_stock=quantite_stock,
            )

            created += 1
            if created % 50 == 0 or created == count:
                self.stdout.write(self.style.SUCCESS(f'Created {created}/{count} medications (last: {nom})'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created} medications (target={count}).'))


