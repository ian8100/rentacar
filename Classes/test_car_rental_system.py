import unittest
from datetime import datetime, timedelta
from CarRentalSystem import CarRentalSystem
from Vehicule import Car, Truck, Motorcycle, Vehicule
from Customer import Customer
from Rental import Rental

class TestCarRentalSystem(unittest.TestCase):
    """
    Suite de tests unitaires pour la classe CarRentalSystem.
    
    Cette classe teste les fonctionnalités principales du système :
    - Gestion du cycle de vie des véhicules (ajout, suppression, maintenance).
    - Gestion des clients et de leur éligibilité.
    - Cycle de vie complet des locations (création, fin, pénalités, extension).
    - Génération des rapports financiers et d'état.
    """

    def setUp(self):
        """
        Configuration initiale exécutée avant chaque test.
        
        Initialise :
        - Une instance fraîche de CarRentalSystem.
        - Des dates de référence (aujourd'hui, passé, futur) pour simuler 
        des durées de location cohérentes.
        """
        self.system = CarRentalSystem()

        self.today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.future_date = self.today + timedelta(days=5)
        self.past_date = self.today - timedelta(days=5)
        self.very_future_date = self.today + timedelta(days=10)

    def test_initialization(self):
        """
        Teste l'état initial du système après sa création.
        
        Vérifie que :
        - Les dictionnaires de véhicules et de clients sont vides.
        - Le compteur d'ID de véhicule commence bien à 1.
        """
        self.assertEqual(len(self.system.vehicles), 0)
        self.assertEqual(len(self.system.customers), 0)
        self.assertEqual(self.system.next_vehicle_id, 1)

    def test_add_vehicle_car(self):
        """
        Teste l'ajout d'un véhicule de type 'Car' (Voiture).
        
        Vérifie que :
        - L'objet retourné est bien une instance de la classe Car.
        - L'ID est correctement assigné et incrémenté.
        - Les attributs (prix journalier) sont corrects.
        - Le véhicule est disponible par défaut.
        """
        car = self.system.add_vehicle("Audi", "A4", "car", 50.0)
        self.assertIsInstance(car, Car)
        self.assertEqual(car.vehicle_id, 1)
        self.assertEqual(self.system.next_vehicle_id, 2)
        self.assertEqual(car.daily_rate, 50.0)
        self.assertTrue(car.is_available())

    def test_add_vehicle_truck(self):
        """
        Teste l'ajout d'un véhicule de type 'Truck' (Camion).
        
        Vérifie que :
        - L'objet retourné est bien une instance de Truck.
        - Les attributs spécifiques (capacité de chargement) sont bien enregistrés.
        """
        truck = self.system.add_vehicle("Man", "TGS", "truck", 120.0, payload_capacity=10.0)
        self.assertIsInstance(truck, Truck)
        self.assertEqual(truck.payload_capacity, 10.0)

    def test_remove_available_vehicle(self):
        """
        Teste la suppression d'un véhicule qui n'est pas en location.
        
        Vérifie que :
        - Le véhicule est bien retiré du dictionnaire des véhicules du système.
        """
        car = self.system.add_vehicle("Ford", "Focus", "car", 30.0)
        self.system.remove_vehicle(car.vehicle_id)
        self.assertNotIn(car.vehicle_id, self.system.vehicles)

    def test_remove_non_existent_vehicle(self):
        """
        Teste la tentative de suppression d'un ID de véhicule inconnu.
        
        Vérifie que :
        - Une exception ValueError est levée avec un message approprié.
        """
        with self.assertRaisesRegex(ValueError, "Vehicle 999 not found"):
            self.system.remove_vehicle(999)

    def test_get_available_vehicles(self):
        """
        Teste le filtrage des véhicules disponibles.
        
        Scénario :
        - Ajout de 3 véhicules.
        - Mise en location forcée d'un véhicule.
        
        Vérifie que :
        - La liste retournée contient uniquement les véhicules non loués.
        """
        car1 = self.system.add_vehicle("A", "M1", "car", 50.0)
        car2 = self.system.add_vehicle("B", "M2", "car", 60.0)
        truck = self.system.add_vehicle("C", "M3", "truck", 100.0)

        car2.set_state(Vehicule.RENTED)

        available = self.system.get_available_vehicles()
        self.assertEqual(len(available), 2)
        self.assertIn(car1, available)
        self.assertNotIn(car2, available)
        self.assertIn(truck, available)

    def test_vehicle_maintenance(self):
        """
        Teste le cycle complet de maintenance d'un véhicule.
        
        Vérifie que :
        1. L'état passe à MAINTENANCE après planification.
        2. Il est impossible de supprimer un véhicule en maintenance (simulé ici par le message d'erreur de location, à adapter selon la logique métier stricte).
        3. L'état repasse à AVAILABLE une fois la maintenance terminée.
        """
        car = self.system.add_vehicle("A", "M1", "car", 50.0)
        self.system.schedule_vehicle_maintenance(car.vehicle_id, "Oil change", 2)
        self.assertEqual(car.state, Vehicule.MAINTENANCE)

        with self.assertRaises(ValueError): 
            self.system.remove_vehicle(car.vehicle_id) 

        self.system.complete_vehicle_maintenance(car.vehicle_id)
        self.assertEqual(car.state, Vehicule.AVAILABLE)

    def test_add_customer(self):
        """
        Teste l'ajout d'un nouveau client dans la base de données.
        
        Vérifie que :
        - L'ID client est généré correctement.
        - Les données personnelles sont correctement stockées.
        """
        cust = self.system.add_customer("Jean", "Dupont", 30, "B")
        self.assertEqual(cust.customer_id, 1)
        self.assertEqual(cust.last_name, "Dupont")
        self.assertIn(1, self.system.customers)

    def test_remove_customer(self):
        """
        Teste la suppression d'un client existant.
        
        Vérifie que :
        - Le client est bien retiré du dictionnaire des clients.
        """
        cust = self.system.add_customer("Marie", "Curie", 45, "B")
        self.system.remove_customer(cust.customer_id)
        self.assertNotIn(cust.customer_id, self.system.customers)

    def test_customer_can_rent_vehicle_eligibility(self):
        """
        Teste les règles métier d'éligibilité à la location (Âge et Permis).
        
        Scénarios testés :
        1. Client trop jeune pour une voiture.
        2. Client avec mauvais permis pour un camion.
        3. Client avec bon âge et bon permis pour un camion.
        """
        young_customer = Customer(10, "Young", "One", 14, "B")
        truck_customer = Customer(11, "Truck", "Driver", 25, "C") 

        car = self.system.add_vehicle("CarBrand", "Model", "car", 50.0)
        truck = self.system.add_vehicle("TruckBrand", "TModel", "truck", 100.0)

        self.assertFalse(young_customer.can_rent_vehicle(car))
        self.assertFalse(young_customer.can_rent_vehicle(truck)) 
        self.assertTrue(truck_customer.can_rent_vehicle(truck)) 

    def test_create_rental_success(self):
        """
        Teste la création réussie d'une location standard.
        
        Vérifie que :
        - La location est créée avec le statut ACTIVE.
        - Le coût total prévisionnel est correct (Durée * Prix/jour).
        - L'état du véhicule passe à RENTED.
        """
        car = self.system.add_vehicle("V1", "M1", "car", 50.0)
        cust = self.system.add_customer("C1", "L1", 25, "B")
        
        rental = self.system.create_rental(cust.customer_id, car.vehicle_id, self.today, self.future_date)
        
        self.assertEqual(rental.rental_id, 1)
        self.assertEqual(rental.status, Rental.ACTIVE)
        self.assertAlmostEqual(rental.total_cost, 5 * 50.0)
        self.assertEqual(car.state, Vehicule.RENTED)

    def test_create_rental_unavailable_vehicle(self):
        """
        Teste l'impossibilité de louer un véhicule déjà loué.
        
        Vérifie que :
        - Une ValueError est levée si le véhicule n'est pas AVAILABLE.
        """
        car = self.system.add_vehicle("V1", "M1", "car", 50.0)
        cust = self.system.add_customer("C1", "L1", 25, "B")
        
        car.set_state(Vehicule.RENTED)
        
        with self.assertRaisesRegex(ValueError, "Vehicle 1 is not available"):
            self.system.create_rental(cust.customer_id, car.vehicle_id, self.today, self.future_date)

    def test_create_rental_overlap(self):
        """
        Teste la détection de chevauchement de dates (Double réservation).
        
        Vérifie que :
        - Le système empêche de créer une nouvelle location pour un véhicule
        sur une période qui chevauche une location existante active.
        """
        car = self.system.add_vehicle("V1", "M1", "car", 50.0)
        cust = self.system.add_customer("C1", "L1", 25, "B")

        self.system.create_rental(cust.customer_id, car.vehicle_id, self.today, self.future_date)
        
        overlap_start = self.today + timedelta(days=3)
        overlap_end = self.today + timedelta(days=8)
        
        with self.assertRaisesRegex(ValueError, "Vehicle 1 is already reserved for these dates"):
            self.system.create_rental(cust.customer_id, car.vehicle_id, overlap_start, overlap_end)

    def test_complete_rental_on_time(self):
        """
        Teste la finalisation d'une location retournée à temps.
        
        Vérifie que :
        - Le statut de la location passe à COMPLETED.
        - Le véhicule redevient AVAILABLE.
        - Aucune pénalité n'est appliquée.
        - L'historique et les dépenses du client sont mis à jour.
        """
        car = self.system.add_vehicle("V1", "M1", "car", 50.0)
        cust = self.system.add_customer("C1", "L1", 25, "B")
        rental = self.system.create_rental(cust.customer_id, car.vehicle_id, self.today, self.future_date)

        return_date = self.future_date - timedelta(hours=1)
        self.system.complete_rental(rental.rental_id, return_date)

        self.assertEqual(rental.status, Rental.COMPLETED)
        self.assertEqual(car.state, Vehicule.AVAILABLE)
        self.assertEqual(rental.late_return_penalty, 0.0)
        self.assertEqual(cust.get_rental_count(), 1)
        self.assertAlmostEqual(cust.total_spent, rental.total_cost)

    def test_complete_rental_late(self):
        """
        Teste la finalisation d'une location retournée en retard.
        
        Vérifie que :
        - La pénalité de retard est correctement calculée (Jours retard * Tarif * %Pénalité).
        - Le coût total inclut le coût initial + la pénalité.
        """
        car = self.system.add_vehicle("V1", "M1", "car", 50.0)
        cust = self.system.add_customer("C1", "L1", 25, "B")
        rental = self.system.create_rental(cust.customer_id, car.vehicle_id, self.today, self.future_date)

        late_return_date = self.future_date + timedelta(days=2, hours=1)
        self.system.complete_rental(rental.rental_id, late_return_date)

        expected_penalty = 2 * 50.0 * Rental.LATE_RETURN_PENALTY_PERCENT
        initial_cost = 5 * 50.0 
        
        self.assertEqual(rental.status, Rental.COMPLETED)
        self.assertAlmostEqual(rental.late_return_penalty, expected_penalty)
        self.assertAlmostEqual(rental.total_cost, initial_cost + expected_penalty)

    def test_extend_rental(self):
        """
        Teste la fonctionnalité d'extension de la durée d'une location.
        
        Vérifie que :
        - La date de fin est mise à jour.
        - Le coût total est recalculé en fonction de la nouvelle durée.
        """
        car = self.system.add_vehicle("V1", "M1", "car", 50.0)
        cust = self.system.add_customer("C1", "L1", 25, "B")
        rental = self.system.create_rental(cust.customer_id, car.vehicle_id, self.today, self.future_date)
        
        self.system.extend_rental(rental.rental_id, self.very_future_date)
        
        self.assertEqual(rental.end_date, self.very_future_date)
        self.assertAlmostEqual(rental.total_cost, 10 * 50.0) 

    def test_is_overdue(self):
        """
        Teste la détection des locations en retard.
        
        Vérifie que :
        - Une location active dont la date de fin est passée retourne True.
        """
        car = self.system.add_vehicle("V1", "M1", "car", 50.0)
        cust = self.system.add_customer("C1", "L1", 25, "B")
        
        past_end_date = self.today - timedelta(days=1)
        past_start_date = self.past_date
        rental_overdue = Rental(99, cust, car, past_start_date, past_end_date)
        rental_overdue.status = Rental.ACTIVE 
        
        self.assertTrue(rental_overdue.is_overdue())

    def test_generate_fleet_report(self):
        """
        Teste la précision des statistiques du rapport de flotte.
        
        Vérifie que le rapport compte correctement :
        - Le nombre total de véhicules.
        - La répartition par état (Disponible, Loué, Maintenance).
        - La répartition par type (Voiture, Camion, etc.).
        """
        car1 = self.system.add_vehicle("A", "M1", "car", 50.0)
        car2 = self.system.add_vehicle("B", "M2", "car", 60.0)
        truck = self.system.add_vehicle("C", "M3", "truck", 100.0)
        
        self.system.schedule_vehicle_maintenance(car2.vehicle_id, "Inspection") 
        self.system.create_rental(
            self.system.add_customer("C1", "L1", 30, "B").customer_id, 
            car1.vehicle_id, 
            self.today, 
            self.future_date
        ) 
        
        report = self.system.generate_fleet_report()
        
        self.assertEqual(report['total_vehicles'], 3)
        self.assertEqual(report['available'], 1) 
        self.assertEqual(report['rented'], 1) 
        self.assertEqual(report['in_maintenance'], 1) 
        self.assertEqual(report['vehicles_by_type']['cars'], 2)
        self.assertEqual(report['vehicles_by_type']['trucks'], 1)

    def test_generate_revenue_report(self):
        """
        Teste la précision des calculs financiers du rapport de revenus.
        
        Simule deux locations (une à temps, une en retard) et vérifie :
        - Le revenu total.
        - Le montant total des pénalités.
        - Le revenu de base (sans pénalités).
        """
        car = self.system.add_vehicle("V1", "M1", "car", 50.0)
        cust = self.system.add_customer("C1", "L1", 25, "B")
        
        rental1 = self.system.create_rental(cust.customer_id, car.vehicle_id, self.today, self.future_date)
        self.system.complete_rental(rental1.rental_id, self.future_date)
        
        rental2_start = self.future_date + timedelta(days=1)
        rental2_end = rental2_start + timedelta(days=5)
        car.set_state(Vehicule.AVAILABLE) 
        rental2 = self.system.create_rental(cust.customer_id, car.vehicle_id, rental2_start, rental2_end)
        self.system.complete_rental(rental2.rental_id, rental2_end + timedelta(days=1, hours=1))
        
        report = self.system.generate_revenue_report()
        
        total_revenue = 250.0 + 275.0
        total_penalties = 25.0 
        base_revenue = 500.0
        
        self.assertEqual(report['total_rentals'], 2)
        self.assertAlmostEqual(report['total_revenue'], total_revenue)
        self.assertAlmostEqual(report['total_penalties'], total_penalties)
        self.assertAlmostEqual(report['base_revenue'], base_revenue)

if __name__ == '__main__':
    unittest.main()
