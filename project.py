import itertools
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Définir les caractères à utiliser dans le mot de passe
characters = string.ascii_letters + string.digits + string.punctuation

# Fonction pour générer des mots de passe et tester si c'est le bon
def test_password(attempts, password, start_time):
    for attempt in attempts:
        current_pass = ''.join(attempt)
        if current_pass == password:
            print(f"Mot de passe trouvé: {current_pass} en {time.time() - start_time} secondes")
            return True
    return False

# Fonction brute force avec parallélisation
def brute_force(password):
    start_time = time.time()
    print_time = start_time

    with ThreadPoolExecutor() as executor:
        futures = []
        # Itérer sur la longueur des mots de passe de 1 à une longueur arbitraire
        for length in range(1, len(password) + 1):
            # Créer des lots de tentatives à traiter en parallèle
            all_attempts = list(itertools.product(characters, repeat=length))
            batch_size = 10000  # Taille de chaque lot
            for i in range(0, len(all_attempts), batch_size):
                batch = all_attempts[i:i+batch_size]
                future = executor.submit(test_password, batch, password, start_time)
                futures.append(future)
            
            # Vérification des résultats et mise à jour de l'affichage
            for future in as_completed(futures):
                current_time = time.time()
                if future.result():
                    return
                if current_time - print_time >= 10:
                    print(f"Temps écoulé: {int(current_time - start_time)}s")
                    print_time = current_time

# Exemple d'utilisation
brute_force("test@1")
