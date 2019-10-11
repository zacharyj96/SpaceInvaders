import sys

import pygame
import random

from bullet import Bullet
from alien import Alien
from alienbullet import Alienbullet
from explosion import Explosion
from ufo import Ufo


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    # Respond to keypresses
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    # Fire a bullet if limit not reached yet
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def fire_alien_bullet(ai_settings, screen, alien, alienbullets):
    new_bullet = Alienbullet(ai_settings, screen, alien)
    alienbullets.add(new_bullet)


def check_keyup_events(event, ship):
    # Respond to key releases
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alienbullets, explosions, ufos):
    # Respond to keypresses and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y, alienbullets, explosions, ufos)

    randufonum = random.randint(1, 5000)
    if randufonum == 5 and not ufos:
        ufo = Ufo(ai_settings, screen)
        ufos.add(ufo)

    randintnum = random.randint(1, ai_settings.alien_bullet_prob)
    if randintnum == 5:
        randaliennum = random.randint(0, len(aliens) - 1)
        i = 0
        for alien in aliens:
            if i == randaliennum:
                fire_alien_bullet(ai_settings, screen, alien, alienbullets)
            i = i + 1


def check_play_button(ai_settings, screen, stats, sb, play_button,
                      ship, aliens, bullets, mouse_x, mouse_y, alienbullets, explosions, ufos):
    # Start a new game when the player clicks Play
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        alienbullets.empty()
        explosions.empty()
        ufos.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, alienbullets, explosions, ufos):
    # Update images on the screen and flip to the new screen
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for alienbullet in alienbullets.sprites():
        alienbullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    explosions.draw(screen)
    ufos.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()


def update_explosions(explosions):
    explosions.update()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alienbullets, explosions, ufos):
    # Update position of bullets and get rid of old bullets
    # Update bullet positions
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, alienbullets, explosions, ufos)


def update_alien_bullets(ai_settings, screen, stats, sb, ship,
                         aliens, bullets, alienbullets, explosions, ufos):
    alienbullets.update()

    for alienbullet in alienbullets.copy():
        if alienbullet.rect.top >= 800:
            alienbullets.remove(alienbullet)

    check_alien_bullet_ship_collisions(ai_settings, screen, stats, sb,
                                       ship, aliens, bullets, alienbullets, explosions, ufos)


def check_alien_bullet_ship_collisions(ai_settings, screen, stats, sb,
                                       ship, aliens, bullets, alienbullets, explosions, ufos):
    collisions = pygame.sprite.spritecollide(ship, alienbullets, True)

    if collisions:
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alienbullets, explosions, ufos)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets, alienbullets, explosions, ufos):
    # Respond to bullet-alien collisions
    # Remove any bullets and aliens that have collided
    collisionsufos = pygame.sprite.groupcollide(bullets, ufos, True, True)

    if collisionsufos:
        for ufos in collisionsufos.values():
            for ufo in ufos:
                explosion = Explosion(ai_settings, screen, False, True)
                explosion.x = ufo.x
                explosion.rect.x = ufo.rect.x
                explosion.rect.y = ufo.rect.y
                explosions.add(explosion)
                stats.score += ai_settings.ufo_points
            sb.prep_score()
        check_high_score(stats, sb)

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                explosion = Explosion(ai_settings, screen, True, False)
                explosion.x = alien.x
                explosion.rect.x = alien.rect.x
                explosion.rect.y = alien.rect.y
                explosions.add(explosion)

                if alien.alientype == "type1":
                    stats.score += ai_settings.alien_points1
                elif alien.alientype == "type2":
                    stats.score += ai_settings.alien_points2
                elif alien.alientype == "type3":
                    stats.score += ai_settings.alien_points3
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level
        bullets.empty()
        alienbullets.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    # Determine the number of aliens that fit in a row
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    # Determine the number of rows of aliens that fit on the screen
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number, alientype):
    # Create an alien and place it in a row
    alien = Alien(ai_settings, screen, alientype)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    # Create a full fleet of aliens
    # Create an alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen, "type1")
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens
    for row_number in range(number_rows):
        if row_number % 3 == 0:
            for alien_number in range(number_aliens_x):
                create_alien(ai_settings, screen, aliens, alien_number, row_number, "type1")
        elif row_number % 3 == 1:
            for alien_number in range(number_aliens_x):
                create_alien(ai_settings, screen, aliens, alien_number, row_number, "type2")
        elif row_number % 3 == 2:
            for alien_number in range(number_aliens_x):
                create_alien(ai_settings, screen, aliens, alien_number, row_number, "type3")


def check_fleet_edges(ai_settings, aliens):
    # Respond appropriately if any aliens have reached an edge
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    # Drop the entire fleet and change the fleet's direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alienbullets, explosions, ufos):
    # Respond to ship being hit by alien
    explosion = Explosion(ai_settings, screen, False, False)
    explosion.x = ship.rect.x
    explosion.rect.x = ship.rect.x
    explosion.rect.y = ship.rect.y
    explosions.add(explosion)
    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        alienbullets.empty()
        ufos.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, alienbullets, explosions, ufos):
    # Check if any aliens have reached the bottom of the screen
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alienbullets, explosions, ufos)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alienbullets, explosions, ufos):
    # Check if the fleet is at an edge, and then update the positions of all aliens in the fleet
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    ufos.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alienbullets, explosions, ufos)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, alienbullets, explosions, ufos)


def check_high_score(stats, sb):
    # Check to see if there's a new high score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
