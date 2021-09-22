from RFEM.initModel import *
from RFEM.enums import *
from enum import Enum
from math import *

class FreeLoad():

    def ConcentratedLoad(self,
                 no: int = 1,
                 load_case_no: int = 1,
                 surfaces_no = '1',
                 load_direction = FreeConcentratedLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z,
                 load_projection = FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                 load_type = FreeConcentratedLoadLoadType.LOAD_TYPE_FORCE,
                 load_parameter = [1000, 0, 0],
                 comment: str = '',
                 params: dict = {}):
                 
        '''
        for load_projection = FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV:
            load_parameter = [magnitude, X, Y]

        for load_projection = FreeLoadLoadProjection.LOAD_PROJECTION_YZ_OR_VW:
            load_parameter = [magnitude, Y, Z]

        for load_projection = FreeLoadLoadProjection.LOAD_PROJECTION_XZ_OR_UW:
            load_parameter = [magnitude, X, Z]
        '''

        # Client model | Free Concentrated Load
        clientObject = clientModel.factory.create('ns0:free_concentrated_load')

        # Clears object attributes | Sets all attributes to None
        clearAtributes(clientObject)

        # Load No.
        clientObject.no = no
        
        # Load Case No.
        clientObject.load_case = load_case_no
        
        # Assigned Surfaces No.
        clientObject.surfaces = ConvertToDlString(surfaces_no)
        
        # Load Projection
        clientObject.load_projection = load_projection.name
        
        # Load Direction
        clientObject.load_direction = load_direction.name
        
        # Load Parameter
        if len(load_parameter) != 3:
            raise Exception('WARNING: The load parameter needs to be of length 3. Kindly check list inputs for completeness and correctness.')
        clientObject.magnitude = load_parameter[0]
        clientObject.load_location_x = load_parameter[1]
        clientObject.load_location_y = load_parameter[2]

        # Load Type
        clientObject.load_type = load_type.name

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        for key in params:
            clientObject[key] = params[key]

        # Add Free Concentrated Load to client model          
        clientModel.service.set_free_concentrated_load(load_case_no, clientObject)

    def LineLoad(self,
                 no: int = 1,
                 load_case_no: int = 1,
                 surfaces_no = '1',
                 load_direction = FreeLineLoadLoadDirection.LOAD_DIRECTION_LOCAL_Z,
                 load_distribution = FreeLineLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM,
                 load_projection = FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                 load_parameter = [],
                 comment: str = '',
                 params: dict = {}):
                 
        '''
        for load_distribution = FreeLineLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM:
            load_parameter = [magnitude_uniform, load_location_first_x, load_location_first_y, load_location_second_x, load_location_second_y]

        for load_distribution = FreeLineLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR:
            load_parameter = [magnitude_first, magnitude_second, load_location_first_x, load_location_first_y, load_location_second_x, load_location_second_y]
        '''

        # Client model | Free Concentrated Load
        clientObject = clientModel.factory.create('ns0:free_line_load')

        # Clears object attributes | Sets all attributes to None
        clearAtributes(clientObject)

        # Load No.
        clientObject.no = no
        
        # Load Case No.
        clientObject.load_case = load_case_no
        
        # Assigned Surfaces No.
        clientObject.surfaces = ConvertToDlString(surfaces_no)
        
        # Load Distribution
        clientObject.load_distribution = load_distribution.name
        
        # Load Projection
        clientObject.load_projection = load_projection.name
        
        # Load Direction
        clientObject.load_direction = load_direction.name
        
        # Load Parameter
        if load_distribution.name == 'LOAD_DISTRIBUTION_UNIFORM':
            if len(load_parameter) != 5:
                raise Exception('WARNING: The load parameter needs to be of length 5. Kindly check list inputs for completeness and correctness.')
            clientObject.magnitude_uniform = load_parameter[0]
            clientObject.load_location_first_x = load_parameter[1]
            clientObject.load_location_first_y = load_parameter[2]
            clientObject.load_location_second_x = load_parameter[3]
            clientObject.load_location_second_y = load_parameter[4]
        elif load_distribution.name == 'LOAD_DISTRIBUTION_LINEAR':
            if len(load_parameter) != 6:
                raise Exception('WARNING: The load parameter needs to be of length 6. Kindly check list inputs for completeness and correctness.')
            clientObject.magnitude_first = load_parameter[0]
            clientObject.magnitude_second = load_parameter[1]
            clientObject.load_location_first_x = load_parameter[2]
            clientObject.load_location_first_y = load_parameter[3]
            clientObject.load_location_second_x = load_parameter[4]
            clientObject.load_location_second_y = load_parameter[5]

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        for key in params:
            clientObject[key] = params[key]

        # Add Free Concentrated Load to client model          
        clientModel.service.set_free_line_load(load_case_no, clientObject)

    def RectangularLoad(self,
                 no: int = 1,
                 load_case_no: int = 1,
                 surfaces_no = '1',
                 load_distribution = FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM,
                 load_projection = FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                 load_direction = FreeRectangularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                 load_magnitude_parameter = [],
                 load_location = FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CORNER_POINTS,
                 load_location_parameter = [],
                 comment: str = '',
                 params: dict = {}):
                 
        '''
        for load_distribution = FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM:
            load_magnitude_parameter = [magnitude_uniform]

        for load_distribution = FreeLineLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_FIRST or FreeLineLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_SECOND:
            load_magnitude_parameter = [magnitude_linear_first, magnitude_linear_second]
        
        for load_location = FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CORNER_POINTS:
            
            for load_distribution = FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM or FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_FIRST or FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_SECOND:
                load_location_parameter = [load_location_first_x, load_location_first_y, load_location_second_x, load_location_second_y, axis_start_angle]
            
            for load_distribution = FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_VARYING_IN_Z:
                    load_location_parameter = [load_location_first_x, load_location_first_y, load_location_second_x, load_location_second_y, [[distance, factor], ...]

            for load_distribution = FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_VARYING_ALONG_PERIMETER:
                    load_location_parameter = [load_location_first_x, load_location_first_y, load_location_second_x, load_location_second_y, [axis_definition_p1_x, axis_definition_p1_y, axis_definition_p1_z], [axis_definition_p2_x, axis_definition_p2_y, axis_definition_p2_z], axis_start_angle,[[alpha, factor], ...]

            for load_distribution = FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_VARYING_IN_Z_AND_ALONG_PERIMETER:
                    load_location_parameter = [load_location_first_x, load_location_first_y, load_location_second_x, load_location_second_y, [[distance, factor], ...], [axis_definition_p1_x, axis_definition_p1_y, axis_definition_p1_z], [axis_definition_p2_x, axis_definition_p2_y, axis_definition_p2_z], axis_start_angle,[[alpha, factor], ...]
        
        for load_location = FreeRectangularLoadLoadLocationRectangle.LOAD_LOCATION_RECTANGLE_CENTER_AND_SIDES:
            
            for load_distribution = FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM or FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_FIRST or FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_SECOND:
                load_location_parameter = [load_location_center_x, load_location_center_y, load_location_center_side_a, load_location_center_side_b, axis_start_angle]
            
            for load_distribution = FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_VARYING_IN_Z:
                    load_location_parameter = [load_location_center_x, load_location_center_y, load_location_center_side_a, load_location_center_side_b, [[distance, factor], ...]

            for load_distribution = FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_VARYING_ALONG_PERIMETER:
                    load_location_parameter = [load_location_center_x, load_location_center_y, load_location_center_side_a, load_location_center_side_b, [axis_definition_p1_x, axis_definition_p1_y, axis_definition_p1_z], [axis_definition_p2_x, axis_definition_p2_y, axis_definition_p2_z], axis_start_angle,[[alpha, factor], ...]

            for load_distribution = FreeRectangularLoadLoadDistribution.LOAD_DISTRIBUTION_VARYING_IN_Z_AND_ALONG_PERIMETER:
                    load_location_parameter = [load_location_center_x, load_location_center_y, load_location_center_side_a, load_location_center_side_b, [[distance, factor], ...], [axis_definition_p1_x, axis_definition_p1_y, axis_definition_p1_z], [axis_definition_p2_x, axis_definition_p2_y, axis_definition_p2_z], axis_start_angle,[[alpha, factor], ...]
        '''

        # Client model | Free Concentrated Load
        clientObject = clientModel.factory.create('ns0:free_rectangular_load')

        # Clears object attributes | Sets all attributes to None
        clearAtributes(clientObject)

        # Load No.
        clientObject.no = no
        
        # Load Case No.
        clientObject.load_case = load_case_no
        
        # Assigned Surfaces No.
        clientObject.surfaces = ConvertToDlString(surfaces_no)
        
        # Load Distribution
        clientObject.load_distribution = load_distribution.name
        
        # Load Projection
        clientObject.load_projection = load_projection.name
        
        # Load Direction
        clientObject.load_direction = load_direction.name
        
        # Load Magnitude Parameter
        if load_distribution.name == 'LOAD_DISTRIBUTION_UNIFORM' or load_distribution.name == 'LOAD_DISTRIBUTION_VARYING_IN_Z' or load_distribution.name == 'LOAD_DISTRIBUTION_VARYING_ALONG_PERIMETER' or load_distribution.name == 'LOAD_DISTRIBUTION_VARYING_IN_Z_AND_ALONG_PERIMETER':
            if len(load_magnitude_parameter) != 1:
                raise Exception('WARNING: The load parameter for the selected distribution needs to be of length 1. Kindly check list inputs for completeness and correctness.')
            clientObject.magnitude_uniform = load_magnitude_parameter[0]

        elif load_distribution.name == 'LOAD_DISTRIBUTION_LINEAR_FIRST' or load_distribution.name == 'LOAD_DISTRIBUTION_LINEAR_SECOND':
            if len(load_magnitude_parameter) != 2:
                raise Exception('WARNING: The load parameter for the selected distribution needs to be of length 2. Kindly check list inputs for completeness and correctness.')
            clientObject.magnitude_linear_first = load_magnitude_parameter[0]
            clientObject.magnitude_linear_second = load_magnitude_parameter[1]

        # Load Location Parameter
        clientObject.load_location_rectangle = load_location.name

        if load_location.name == 'LOAD_LOCATION_RECTANGLE_CORNER_POINTS':

            if load_distribution.name == 'LOAD_DISTRIBUTION_UNIFORM' or load_distribution.name == 'LOAD_DISTRIBUTION_LINEAR_FIRST' or load_distribution.name == 'LOAD_DISTRIBUTION_LINEAR_SECOND':
                if len(load_location_parameter) != 5:
                    raise Exception('WARNING: The load location parameter for the designated location and distribution type needs to be of length 5. Kindly check list inputs for completeness and correctness.')
                clientObject.load_location_first_x = load_location_parameter[0]
                clientObject.load_location_first_y = load_location_parameter[1]
                clientObject.load_location_second_x = load_location_parameter[2]
                clientObject.load_location_second_y = load_location_parameter[3]
                clientObject.axis_start_angle = load_location_parameter[4] * (pi/180)

            elif load_distribution.name == 'LOAD_DISTRIBUTION_VARYING_IN_Z':
                if len(load_location_parameter) != 5:
                    raise Exception('WARNING: The load location parameter for the designated location and distribution type needs to be of length 5. Kindly check list inputs for completeness and correctness.')
                clientObject.load_location_first_x = load_location_parameter[0]
                clientObject.load_location_first_y = load_location_parameter[1]
                clientObject.load_location_second_x = load_location_parameter[2]
                clientObject.load_location_second_y = load_location_parameter[3]

                clientObject.load_varying_in_z_parameters = clientModel.factory.create('ns0:free_rectangular_load.load_varying_in_z_parameters')
                varying_in_z = load_location_parameter[4]
                for i in range(len(varying_in_z)):
                    frllvp = clientModel.factory.create('ns0:free_rectangular_load_load_varying_in_z_parameters')
                    frllvp.no = i+1
                    frllvp.distance = varying_in_z[i][0]
                    frllvp.factor = varying_in_z[i][1]
                    clientObject.load_varying_in_z_parameters.free_rectangular_load_load_varying_in_z_parameters.append(frllvp)

            elif load_distribution.name == 'LOAD_DISTRIBUTION_VARYING_ALONG_PERIMETER':
                if len(load_location_parameter) != 8:
                    raise Exception('WARNING: The load location parameter for the designated location and distribution type needs to be of length 9. Kindly check list inputs for completeness and correctness.')
                clientObject.load_location_first_x = load_location_parameter[0]
                clientObject.load_location_first_y = load_location_parameter[1]
                clientObject.load_location_second_x = load_location_parameter[2]
                clientObject.load_location_second_y = load_location_parameter[3]
                clientObject.axis_definition_p1_x = load_location_parameter[4][0]
                clientObject.axis_definition_p1_y = load_location_parameter[4][1]
                clientObject.axis_definition_p1_z = load_location_parameter[4][2]
                clientObject.axis_definition_p2_x = load_location_parameter[5][0]
                clientObject.axis_definition_p2_y = load_location_parameter[5][1]
                clientObject.axis_definition_p2_z = load_location_parameter[5][2]
                clientObject.axis_start_angle = load_location_parameter[6]

                clientObject.load_varying_along_perimeter_parameters = clientModel.factory.create('ns0:free_rectangular_load.load_varying_along_perimeter_parameters')
                varying_along_perimeter = load_location_parameter[7]
                for i in range(len(varying_along_perimeter)):
                    frllvapp = clientModel.factory.create('ns0:free_rectangular_load_load_varying_along_perimeter_parameters')
                    frllvapp.no = i+1
                    frllvapp.alpha = varying_along_perimeter[i][0] * (pi/180)    
                    frllvapp.factor = varying_along_perimeter[i][1]
                    clientObject.load_varying_along_perimeter_parameters.free_rectangular_load_load_varying_along_perimeter_parameters.append(frllvapp)

            elif load_distribution.name == 'LOAD_DISTRIBUTION_VARYING_IN_Z_AND_ALONG_PERIMETER':
                if len(load_location_parameter) != 9:
                    raise Exception('WARNING: The load location parameter for the designated location and distribution type needs to be of length 9. Kindly check list inputs for completeness and correctness.')
                clientObject.load_location_first_x = load_location_parameter[0]
                clientObject.load_location_first_y = load_location_parameter[1]
                clientObject.load_location_second_x = load_location_parameter[2]
                clientObject.load_location_second_y = load_location_parameter[3]

                clientObject.load_varying_in_z_parameters = clientModel.factory.create('ns0:free_rectangular_load.load_varying_in_z_parameters')
                varying_in_z = load_location_parameter[4]
                for i in range(len(varying_in_z)):
                    frllvp = clientModel.factory.create('ns0:free_rectangular_load_load_varying_in_z_parameters')
                    frllvp.no = i+1
                    frllvp.distance = varying_in_z[i][0]
                    frllvp.factor = varying_in_z[i][1]
                    clientObject.load_varying_in_z_parameters.free_rectangular_load_load_varying_in_z_parameters.append(frllvp)

                clientObject.axis_definition_p1_x = load_location_parameter[5][0]
                clientObject.axis_definition_p1_y = load_location_parameter[5][1]
                clientObject.axis_definition_p1_z = load_location_parameter[5][2]
                clientObject.axis_definition_p2_x = load_location_parameter[6][0]
                clientObject.axis_definition_p2_y = load_location_parameter[6][1]
                clientObject.axis_definition_p2_z = load_location_parameter[6][2]
                clientObject.axis_start_angle = load_location_parameter[7]

                clientObject.load_varying_along_perimeter_parameters = clientModel.factory.create('ns0:free_rectangular_load.load_varying_along_perimeter_parameters')
                varying_along_perimeter = load_location_parameter[8]
                for i in range(len(varying_along_perimeter)):
                    frllvapp = clientModel.factory.create('ns0:free_rectangular_load_load_varying_along_perimeter_parameters')
                    frllvapp.no = i+1
                    frllvapp.alpha = varying_along_perimeter[i][0] * (pi/180)
                    frllvapp.factor = varying_along_perimeter[i][1]
                    clientObject.load_varying_along_perimeter_parameters.free_rectangular_load_load_varying_along_perimeter_parameters.append(frllvapp)

        elif load_location.name == 'LOAD_LOCATION_RECTANGLE_CENTER_AND_SIDES':
    
            if load_distribution.name == 'LOAD_DISTRIBUTION_UNIFORM' or load_distribution.name == 'LOAD_DISTRIBUTION_LINEAR_FIRST' or load_distribution.name == 'LOAD_DISTRIBUTION_LINEAR_SECOND':
                if len(load_location_parameter) != 5:
                    raise Exception('WARNING: The load location parameter for the designated location and distribution type needs to be of length 5. Kindly check list inputs for completeness and correctness.')
                clientObject.load_location_center_x = load_location_parameter[0]
                clientObject.load_location_center_y = load_location_parameter[1]
                clientObject.load_location_center_side_a = load_location_parameter[2]
                clientObject.load_location_center_side_b = load_location_parameter[3]
                clientObject.axis_start_angle = load_location_parameter[4] * (pi/180)

            elif load_distribution.name == 'LOAD_DISTRIBUTION_VARYING_IN_Z':
                if len(load_location_parameter) != 5:
                    raise Exception('WARNING: The load location parameter for the designated location and distribution type needs to be of length 5. Kindly check list inputs for completeness and correctness.')
                clientObject.load_location_center_x = load_location_parameter[0]
                clientObject.load_location_center_y = load_location_parameter[1]
                clientObject.load_location_center_side_a = load_location_parameter[2]
                clientObject.load_location_center_side_b = load_location_parameter[3]

                clientObject.load_varying_in_z_parameters = clientModel.factory.create('ns0:free_rectangular_load.load_varying_in_z_parameters')
                varying_in_z = load_location_parameter[4]
                for i in range(len(varying_in_z)):
                    frllvp = clientModel.factory.create('ns0:free_rectangular_load_load_varying_in_z_parameters')
                    frllvp.no = i+1
                    frllvp.distance = varying_in_z[i][0]
                    frllvp.factor = varying_in_z[i][1]
                    clientObject.load_varying_in_z_parameters.free_rectangular_load_load_varying_in_z_parameters.append(frllvp)

            elif load_distribution.name == 'LOAD_DISTRIBUTION_VARYING_ALONG_PERIMETER':
                if len(load_location_parameter) != 8:
                    raise Exception('WARNING: The load location parameter for the designated location and distribution type needs to be of length 9. Kindly check list inputs for completeness and correctness.')
                clientObject.load_location_center_x = load_location_parameter[0]
                clientObject.load_location_center_y = load_location_parameter[1]
                clientObject.load_location_center_side_a = load_location_parameter[2]
                clientObject.load_location_center_side_b = load_location_parameter[3]
                clientObject.axis_definition_p1_x = load_location_parameter[4][0]
                clientObject.axis_definition_p1_y = load_location_parameter[4][1]
                clientObject.axis_definition_p1_z = load_location_parameter[4][2]
                clientObject.axis_definition_p2_x = load_location_parameter[5][0]
                clientObject.axis_definition_p2_y = load_location_parameter[5][1]
                clientObject.axis_definition_p2_z = load_location_parameter[5][2]
                clientObject.axis_start_angle = load_location_parameter[6]

                clientObject.load_varying_along_perimeter_parameters = clientModel.factory.create('ns0:free_rectangular_load.load_varying_along_perimeter_parameters')
                varying_along_perimeter = load_location_parameter[7]
                for i in range(len(varying_along_perimeter)):
                    frllvapp = clientModel.factory.create('ns0:free_rectangular_load_load_varying_along_perimeter_parameters')
                    frllvapp.no = i+1
                    frllvapp.alpha = varying_along_perimeter[i][0] * (pi/180)    
                    frllvapp.factor = varying_along_perimeter[i][1]
                    clientObject.load_varying_along_perimeter_parameters.free_rectangular_load_load_varying_along_perimeter_parameters.append(frllvapp)

            elif load_distribution.name == 'LOAD_DISTRIBUTION_VARYING_IN_Z_AND_ALONG_PERIMETER':
                if len(load_location_parameter) != 9:
                    raise Exception('WARNING: The load location parameter for the designated location and distribution type needs to be of length 9. Kindly check list inputs for completeness and correctness.')
                clientObject.load_location_center_x = load_location_parameter[0]
                clientObject.load_location_center_y = load_location_parameter[1]
                clientObject.load_location_center_side_a = load_location_parameter[2]
                clientObject.load_location_center_side_b = load_location_parameter[3]

                clientObject.load_varying_in_z_parameters = clientModel.factory.create('ns0:free_rectangular_load.load_varying_in_z_parameters')
                varying_in_z = load_location_parameter[4]
                for i in range(len(varying_in_z)):
                    frllvp = clientModel.factory.create('ns0:free_rectangular_load_load_varying_in_z_parameters')
                    frllvp.no = i+1
                    frllvp.distance = varying_in_z[i][0]
                    frllvp.factor = varying_in_z[i][1]
                    clientObject.load_varying_in_z_parameters.free_rectangular_load_load_varying_in_z_parameters.append(frllvp)

                clientObject.axis_definition_p1_x = load_location_parameter[5][0]
                clientObject.axis_definition_p1_y = load_location_parameter[5][1]
                clientObject.axis_definition_p1_z = load_location_parameter[5][2]
                clientObject.axis_definition_p2_x = load_location_parameter[6][0]
                clientObject.axis_definition_p2_y = load_location_parameter[6][1]
                clientObject.axis_definition_p2_z = load_location_parameter[6][2]
                clientObject.axis_start_angle = load_location_parameter[7]

                clientObject.load_varying_along_perimeter_parameters = clientModel.factory.create('ns0:free_rectangular_load.load_varying_along_perimeter_parameters')
                varying_along_perimeter = load_location_parameter[8]
                for i in range(len(varying_along_perimeter)):
                    frllvapp = clientModel.factory.create('ns0:free_rectangular_load_load_varying_along_perimeter_parameters')
                    frllvapp.no = i+1
                    frllvapp.alpha = varying_along_perimeter[i][0] * (pi/180)
                    frllvapp.factor = varying_along_perimeter[i][1]
                    clientObject.load_varying_along_perimeter_parameters.free_rectangular_load_load_varying_along_perimeter_parameters.append(frllvapp)

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        for key in params:
            clientObject[key] = params[key]

        # Add Free Concentrated Load to client model          
        clientModel.service.set_free_rectangular_load(load_case_no, clientObject)

    def CircularLoad(self,
                 no: int = 1,
                 load_case_no: int = 1,
                 surfaces_no = '1',
                 load_distribution = FreeCircularLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM,
                 load_projection = FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                 load_direction = FreeCircularLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                 load_parameter = [],
                 comment: str = '',
                 params: dict = {}):
                 
        '''
        for load_distribution = FreeCircularLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM:
            load_parameter = [magnitude_uniform, load_location_x, load_location_y, load_location_radius]

        for load_distribution = FreeCircularLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR:
            load_parameter = [magnitude_center, magnitude_radius, load_location_x, load_location_y, load_location_radius]
        '''

        # Client model | Free Concentrated Load
        clientObject = clientModel.factory.create('ns0:free_circular_load')

        # Clears object attributes | Sets all attributes to None
        clearAtributes(clientObject)

        # Load No.
        clientObject.no = no
        
        # Load Case No.
        clientObject.load_case = load_case_no
        
        # Assigned Surfaces No.
        clientObject.surfaces = ConvertToDlString(surfaces_no)

        # Load Distribution
        clientObject.load_distribution = load_distribution.name

        # Load Projection
        clientObject.load_projection = load_projection.name
        
        # Load Direction
        clientObject.load_direction = load_direction.name
        
        # Load Parameter
        if load_distribution.name == 'LOAD_DISTRIBUTION_UNIFORM':
            if len(load_parameter) != 4:
                raise Exception('WARNING: The load parameter needs to be of length 4. Kindly check list inputs for completeness and correctness.')
            clientObject.magnitude_uniform = load_parameter[0]
            clientObject.load_location_x = load_parameter[1]
            clientObject.load_location_y = load_parameter[2]
            clientObject.load_location_radius = load_parameter[3]

        elif load_distribution.name == 'LOAD_DISTRIBUTION_LINEAR':
            if len(load_parameter) != 5:
                raise Exception('WARNING: The load parameter needs to be of length 5. Kindly check list inputs for completeness and correctness.')
            clientObject.magnitude_center = load_parameter[0]
            clientObject.magnitude_radius = load_parameter[1]
            clientObject.load_location_x = load_parameter[2]
            clientObject.load_location_y = load_parameter[3]
            clientObject.load_location_radius = load_parameter[4]

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        for key in params:
            clientObject[key] = params[key]

        # Add Free Concentrated Load to client model          
        clientModel.service.set_free_circular_load(load_case_no, clientObject)

    def PolygonLoad(self,
                 no: int = 1,
                 load_case_no: int = 1,
                 surfaces_no = '1',
                 load_distribution = FreePolygonLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM,
                 load_projection = FreeLoadLoadProjection.LOAD_PROJECTION_XY_OR_UV,
                 load_direction = FreePolygonLoadLoadDirection.LOAD_DIRECTION_GLOBAL_Z_TRUE,
                 load_location = [],
                 load_parameter = [],
                 comment: str = '',
                 params: dict = {}):
                 
        '''
        for load_distribution = FreePolygonLoadLoadDistribution.LOAD_DISTRIBUTION_UNIFORM:
            load_location = [[first_coordinate, second_coordinate], ...]
            load_parameter = [magnitude_uniform]

       for load_distribution = FreePolygonLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR:
            load_location = [[first_coordinate, second_coordinate], ...]
            load_parameter = [magnitude_linear_1, magnitude_linear_2, magnitude_linear_3, magnitude_linear_location_1, magnitude_linear_location_2, magnitude_linear_location_3]

       for load_distribution = FreePolygonLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_FIRST:
            load_location = [[first_coordinate, second_coordinate], ...]
            load_parameter = [magnitude_linear_1, magnitude_linear_2, magnitude_linear_location_1, magnitude_linear_location_2]

       for load_distribution = FreePolygonLoadLoadDistribution.LOAD_DISTRIBUTION_LINEAR_SECOND:
            load_location = [[first_coordinate, second_coordinate], ...]
            load_parameter = [magnitude_linear_1, magnitude_linear_2, magnitude_linear_location_1, magnitude_linear_location_2]
        '''

        # Client model | Free Concentrated Load
        clientObject = clientModel.factory.create('ns0:free_polygon_load')

        # Clears object attributes | Sets all attributes to None
        clearAtributes(clientObject)

        # Load No.
        clientObject.no = no
        
        # Load Case No.
        clientObject.load_case = load_case_no
        
        # Assigned Surfaces No.
        clientObject.surfaces = ConvertToDlString(surfaces_no)

        # Load Distribution
        clientObject.load_distribution = load_distribution.name

        # Load Projection
        clientObject.load_projection = load_projection.name
        
        # Load Direction
        clientObject.load_direction = load_direction.name

        # Load Location
        clientObject.load_location = clientModel.factory.create('ns0:free_polygon_load.load_location')
        for i in range(len(load_location)):
            fplld = clientModel.factory.create('ns0:free_polygon_load_load_location')
            fplld.no = i+1
            fplld.first_coordinate = load_location[i][0]
            fplld.second_coordinate = load_location[i][1]
            clientObject.load_location.free_polygon_load_load_location.append(fplld)

        # Load Parameter
        if load_distribution.name == 'LOAD_DISTRIBUTION_UNIFORM':
            if len(load_parameter) != 1:
                raise Exception('WARNING: The load parameter needs to be of length 1. Kindly check list inputs for completeness and correctness.')
            clientObject.magnitude_uniform = load_parameter[0]

        elif load_distribution.name == 'LOAD_DISTRIBUTION_LINEAR':
            if len(load_parameter) != 6:
                raise Exception('WARNING: The load parameter needs to be of length 6. Kindly check list inputs for completeness and correctness.')
            clientObject.magnitude_linear_1 = load_parameter[0]
            clientObject.magnitude_linear_2 = load_parameter[1]
            clientObject.magnitude_linear_3 = load_parameter[2]
            clientObject.magnitude_linear_location_1 = load_parameter[3]
            clientObject.magnitude_linear_location_2 = load_parameter[4]
            clientObject.magnitude_linear_location_3 = load_parameter[5]

        elif load_distribution.name == 'LOAD_DISTRIBUTION_LINEAR_FIRST' or load_distribution.name == 'LOAD_DISTRIBUTION_LINEAR_SECOND':
            if len(load_parameter) != 4:
                raise Exception('WARNING: The load parameter needs to be of length 4. Kindly check list inputs for completeness and correctness.')
            clientObject.magnitude_linear_1 = load_parameter[0]
            clientObject.magnitude_linear_2 = load_parameter[1]
            clientObject.magnitude_linear_location_1 = load_parameter[2]
            clientObject.magnitude_linear_location_2 = load_parameter[3]

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        for key in params:
            clientObject[key] = params[key]

        # Add Free Concentrated Load to client model          
        clientModel.service.set_free_polygon_load(load_case_no, clientObject)
