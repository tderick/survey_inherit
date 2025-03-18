from odoo import models, fields
from odoo.exceptions import UserError

class PartnerWizard(models.TransientModel):
    _name = 'res.partner.wizard'
    _description = 'Partner Wizard'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
   
    def action_assign_partner(self):
        active_id = self.env.context.get('active_id')

        if active_id:
            survey = self.env['survey.survey'].browse(active_id)
            
            if not survey:
                raise UserError("Survey not found!")

            # Specify the partner_id and email in the answer
            additional_vals = {
                'partner_id': self.partner_id.id,
                'email': self.partner_id.email,
            }

            # Create the survey response and use the extra values
            user_input = survey._create_answer(
                user=self.env.user,
                test_entry=False, 
                **additional_vals,
            )

            #  Construct the survey URL
            survey_url = f"/survey/start/{survey.access_token}?answer_token={user_input.access_token}"

            return {
                'type': 'ir.actions.act_url',
                'url': survey_url,
                'target': 'new', 
            }

        return {'type': 'ir.actions.act_window_close'}