import json


from win32con import FALSE

from VoucherUpdate.Update_TallyNarration_XMLReq import response
from odoo import http
from odoo.http import request, Response

class MyAPI(http.Controller):

    @http.route('/api/products',
                auth='public',
                type='http',
                methods=['GET'],
                csrf=False)

    def get_products(self):
        products = request.env['product.product'].sudo().search([('barcode','=',False)])
        data = products.read(['id', 'name', 'list_price','barcode'])

        return Response(
            json.dumps(data),
            content_type='application/json',
            status=200
        )

    # Function to update product with the tally id

    @http.route('/api/updateproduct',
                auth='public',
                type='json',
                methods=['POST'],
                csrf=False)

    def updateproduct(self,**payload):
        productid=payload.get('product_id')
        tallyid=payload.get('tally_id')

        if not productid:

            return {'status':'error','message':'product id not found!!'}

        product = request.env['product.product'].sudo().browse(productid)





        if not product:
            return {
                "status": "error",
                "message": f"Product with ID {productid} not found"
            }

        if tallyid:
            duplicate_tallyid=request.env['product.product'].sudo().search([
            ('barcode', '=', tallyid),
            ('id', '!=', productid)
            ], limit=1)

            if duplicate_tallyid:
                return {
                "status": "error",
                "message": f"barcode already assigned to  {duplicate_tallyid.name} "
            }



        # product=request.env['product.product'].sudo().write({'barcode':tallyid})
        product.sudo().write({
            'barcode': tallyid
        })


        return {
            "status": "success",
            "message": "Tally ID updated successfully",
            "product_id": product.id,
            "tally_id": product.barcode,
            "product_name": product.name
        }

    # end of update

    # Deleteing the product

    @http.route('/api/delete', type='json', auth='public', methods=['POST'], csrf=False)
    def DeleteEntry(self, **payload):
        entry_id = payload.get('recordno')

        getrecord = request.env['sale.order'].sudo().browse(entry_id)
        newrec=getrecord.id
        if not getrecord.exists():
            return {
                'error': 'Error',
                'message': f"record not found with the id  {newrec}"
            }

        getrecord.unlink()
        return {
            'message':'success record deleted'
        }

    # End of Delete Product


    @http.route('/api/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_record(self, **payload):


        name = payload.get('name')

        if not name:
            return {"status": "error", "message": "Name is required"}

        # CHECK IF NAME ALREADY EXISTS
        existing_partner = request.env['res.partner'].sudo().search([('name', '=', name)],limit=1)


        if existing_partner:
            return {
                "status": "error",
                "message": f"Contact '{name}' already exists",
                "partner_id": existing_partner.id,
                "partner_name": existing_partner.name
            }

        # CREATE NEW PARTNER
        partner = request.env['res.partner'].sudo().create({
            'name': name,
        })

        return {
            "status": "success",
            "message": "Contact created successfully",
            "partner_id": partner.id,
            "partner_name": partner.name
        }

#     Some changes made









