# -*- coding: utf-8 -*

from openerp.osv import osv, fields 


class Course (osv.Model):
    _name = 'diego_dev.course'
    
    def get_seats(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        courses = self.browse(cr, uid, ids, context=context)
        for course in courses:
            total_seats = course.total_seats
            students = course.student_ids
            occupied_seats = len(students)
            available_seats = total_seats-occupied_seats
            if total_seats:
                occupation_percentage = (occupied_seats / (total_seats*1.0)) * 100.0
            else:
                occupation_percentage=0.0
            res[course.id] =  {
                               'available_seats':available_seats,
                               'occupied_seats':occupied_seats,
                               'occupation_percentage':occupation_percentage,
            }
        return res     
    
    _columns = {
        'name': fields.char('Name', size=128, required=True, select=True),
        'code': fields.char('Code', size=32, required=True, select=True),
        'description': fields.text('Description'),   
        'session_ids': fields.one2many('diego_dev.course.session','course_id', string='Session'),   
        'student_ids': fields.many2many('res.partner', string='Students',domain=[('student','=',1)],), 
        'teacher_id' : fields.many2one('res.users', string='Teacher', ondelete='set null', select=True),   
        'total_seats': fields.integer('Total seats', required=True),
        'available_seats': fields.function(get_seats, multi='seats',type='integer', string='Available seats',readonly=True),
        'occupied_seats':fields.function(get_seats, multi='seats',type='integer', string='Occupied seats',readonly=True),
        'occupation_percentage':fields.function(get_seats, multi='seats',type='integer', string='Occupation percentage',digits=(3,1), readonly=True),
                }
    _defaults = {
            'teacher_id': (lambda  self, cr, uid, this, context ={}: uid),
            'total_seats': 20,
                }
    
class Partner(osv.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    _columns ={
        'student': fields.boolean('Student'),       
        'birthday': fields.date ('Birthday'), 
        'course_ids': fields.many2many('diego_dev.course', string='Courses'),
        'student_code':fields.char('Student code', size=32),    
               }
    def on_change_is_company(self,cr, uid, id, is_company, student, context = {}):
        res = self.onchange_type(cr,uid, id, is_company, context=context)
        #res = {'value' : {}, 'domain':{}, 'warning':{}}
        if is_company and student:
            res['value'].update = ({'student':False})
            res['warning'].update = ({'title': "Companies cannot be students", 'message' : "You changed the partner type to company. We blanked the student checkbox."})
        return res
    
class CourseSession(osv.Model):
    _name = 'diego_dev.course.session'
    _columns = {
        'subject': fields.char('Subject', size=128, required=True, select=True),
        'start_time': fields.datetime('Start Time', required=True),
        'end_time': fields.datetime('End Time'),
        'course_id':fields.many2one('diego_dev.course', string='Course', required=True, select=True, ondelete='cascade'),
                }
    _rec_name = 'subject'
    _order = 'start_time'