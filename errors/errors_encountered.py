''' "state = attributes.instance_state(instance)
AttributeError: 'float' object has no attribute '_sa_instance_state' '''
# Cette erreur survient quand on essaye d'ajouter un objet de type float à la session SQLAlchemy, ce qui n'est pas possible car
# SQLAlchemy ne sait pas comment gérer les objets qui ne sont pas des instances des classes mappées.
# Dans le code (bank.py), il faut retourner des objets de transaction dans les méthodes deposit, withdraw et transfer, et non des valeurs float ou int.

''' raise exc.UnmappedInstanceError(instance) from err
sqlalchemy.orm.exc.UnmappedInstanceError: Class 'builtins.float' is not mapped '''
# L'erreur UnmappedInstanceError survient généralement lorsqu'on essaie de manipuler un objet qui n'est pas connu du mapper SQLAlchemy,
# ce qui peut se produire pour différentes raisons, notamment en essayant d'ajouter un objet de type incorrect à la session.
# L'erreur est probablement due à une tentative d'ajouter des valeurs (float ou autre) à la session au lieu des instances des modèles SQLAlchemy (Account ou Transaction).
# Les méthodes deposit, withdraw et transfer devraient manipuler des objets de type Account et Transaction, et non des valeurs brutes.