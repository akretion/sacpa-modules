# license agpl-3.0 or later (https://www.gnu.org/licenses/agpl).


def post_init_hook(env):
    hotel_reservation = env["hotel.reservation"].search([])
    hotel_folio = env["hotel.folio"].search([])
    hotel_room = env["hotel.room"].search([])
    for r in hotel_reservation:
        r.company_id = env.company.id
    for f in hotel_folio:
        f.company_id = env.company.id
    for r in hotel_room:
        r.company_id = env.company.id
