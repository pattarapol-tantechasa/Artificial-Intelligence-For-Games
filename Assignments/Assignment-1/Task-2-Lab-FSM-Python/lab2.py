# Variables
states = ['Resting', 'Gathering', 'Crafting']
current_state = 'Resting'

energy = 0
wood = 0

alive = True
running = True
game_time = 0
action_trigger = 5
max_limit = 100

print("---START---")
while running and alive:
    game_time += 1
    
    match(current_state):
        case 'Resting':
            energy += 1
            print("Resting......")
            
            if energy >= action_trigger and wood <= 0:
                current_state = 'Gathering'    
            if energy >= action_trigger and wood > 0:
                current_state = 'Crafting'
                
        case 'Gathering':
            wood += 1
            energy -= 1
            print("Gathering Wood in the Forest")
            
            if energy <= 0:
                current_state = 'Resting'    
            
        case 'Crafting':
            wood -= 1
            energy -= 1
            print("Crafting something with Wood")
            
            if energy <= 0:
                current_state = 'Resting'
                
    if energy < 0:
        alive = False    
    if game_time > max_limit:
        running = False
        
print("---END---")

        
     
