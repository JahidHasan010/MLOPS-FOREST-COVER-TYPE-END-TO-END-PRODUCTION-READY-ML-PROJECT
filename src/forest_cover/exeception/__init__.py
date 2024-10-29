import os, sys

class CustomException(Exception):
    def __init__(self,error_message: Exception, error_detail: sys):
        super().__init__(error_message)
        self.error_message = CustomException.prepare_error_message(error_message,error_detail)

    @staticmethod
    def prepare_error_message(error_message: Exception, error_detail: sys)->str:
        _,_,exc_tb = error_detail.exc_info()
        filename = exc_tb.tb_frame.f_code.co_filename
        line_no = exc_tb.tb_lineno

        err_message = f"Error Occured [{filename}] at line no. [{line_no}] & error message [{error_message}]"
        return err_message

    def __repr__(self):
        return self.error_message

    def __str__(self):
        return self.error_message
    
    
# import os
# import sys

# def error_message_detail(error, error_detail:sys):
#     _, _, exc_tb = error_detail.exc_info()
#     file_name = exc_tb.tb_frame.f_code.co_filename
#     error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
#         file_name, exc_tb.tb_lineno, str(error)
#     )

#     return error_message

# class ForestException(Exception):
#     def __init__(self, error_message, error_detail):
#         """
#         :param error_message: error message in string format
#         """
#         super().__init__(error_message)
#         self.error_message = error_message_detail(
#             error_message, error_detail=error_detail
#         )

#     def __str__(self):
#         return self.error_message