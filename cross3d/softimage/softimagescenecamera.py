##
#	\namespace	blur3d.api.softimage.softimagescenecamera
#
#	\remarks	The SotimageSceneCamera class provides the implementation of the AbstractSceneCamera class as it applies
#				to Softimage scenes
#
#	\author		douglas@blur.com
#	\author		Blur Studio
#	\date		03/15/10
#

import math
import traceback

from PySoftimage import xsi
from blur3d.api.abstract.abstractscenecamera import AbstractSceneCamera
import blur3d.api

#------------------------------------------------------------------------------------------------------------------------

class SoftimageSceneCamera(AbstractSceneCamera):

	#------------------------------------------------------------------------------------------------------------------------
	# 												public methods
	#------------------------------------------------------------------------------------------------------------------------

	def interest(self):
		if self._nativePointer.Interest:
			return blur3d.api.SceneObject(self._scene, self._nativePointer.Interest)
		return None

	def setInterest(self, interest):
		if interest:
			self._nativePointer.Interest = interest.nativePointer()

	def fov(self, rounded=False):
		#TODO: (brendana 9/3/13) should this take account keys and current frame? (dougl 8/26/14) Current frame!
		param_name = '{}.camera.fov'.format(self._nativePointer.FullName)
		prop = xsi.Dictionary.GetObject(param_name)
		fov = prop.Value
		if rounded:
			return int(round(fov))
		return fov

	def matchCamera(self, camera):
		"""
			Match this camera to another one.
		"""
		self.setParameters(camera.parameters())
		self.setViewOptions(camera.viewOptions())
		self.matchTransforms(camera)
		return True

	def filmWidth(self):
		"""
			\remarks	Returns the film_width of the camera in mm.
			\return		film_width (float)
		"""
		width = self._nativePointer.projplanewidth.Value
		# XSI uses inches, convert inches to mm 1in / 25.4mm
		return width * 25.4

	def setFilmWidth(self, width):
		"""
			\remarks	Sets the film_width value for the camera.
			\param		width <float>
			\return		n/a
		"""
		# XSI uses inches, convert inches to mm 1in / 25.4mm
		self._nativePointer.projplanewidth.Value = width / 25.4
		return True

	def filmHeight(self):
		"""
			\remarks	Returns the film_height of the camera in mm.
			\return		film_width (float)
		"""
		height = self._nativePointer.projplaneheight.Value
		# XSI uses inches, convert inches to mm 1in / 25.4mm
		return height * 25.4

	def setFilmHeight(self, height):
		"""
			\remarks	Sets the film_height value for the camera.
			\param		width <float>
			\return		n/a
		"""
		# XSI uses inches, convert inches to mm 1in / 25.4mm
		self._nativePointer.projplaneheight.Value = width / 25.4
		return True

	def lens(self, filmWidth=None, rounded=False):
		if filmWidth:
			fov = math.radians(self.fov())
			lens = (0.5 * float(filmWidth)) / math.tan(fov / 2.0)
		else:
			lens = xsi.GetValue(self.name() + '.camera.projplanedist')
		if rounded:
			return int(round(lens))
		return lens

	def setLens(self, value):
		self._nativePointer.Parameters('projplanedist').Value = value

	def showsFrame(self):
		return xsi.GetValue(self.name() + '.camvis.currenttime')

	def setShowsFrame(self, switch):
		xsi.SetValue(self.name() + '.camvis.currenttime', switch)
		return True

	def setShowsCustomParameters(self, switch):
		xsi.SetValue(self.name() + '.camvis.custominfo', switch)
		return True

	def setHeadLightIsActive(self, switch):
		xsi.SetValue(self.name() + '.camdisp.headlight', switch)
		return True

	def headlightIsActive(self):
		return xsi.GetValue(self.name() + '.camdisp.headlight')

	def pictureRatio(self):
		return self._nativePointer.Parameters('aspect').Value

	def setPictureRatio(self, pictureRatio):
		xsi.setValue(self.name() + '.camera.aspect', pictureRatio)
		#self._nativePointer.Parameters( 'aspect' ).Value = pictureRatio
		return True

	def farClippingPlane(self):
		return self._nativePointer.Parameters('far').Value

	def setFarClippingPlane(self, distance):
		xsi.setValue(self.name() + '.camera.far', distance)
		#self._nativePointer.Parameters( 'far' ).Value = distance
		return True

	def nearClippingPlane(self):
		return self._nativePointer.Parameters('near').Value

	def setNearClippingPlane(self, distance):
		xsi.setValue(self.name() + '.camera.near', distance)
		#self._nativePointer.Parameters( 'near' ).Value = distance
		return True

	def clippingEnabled(self):
		return self.userProps().setdefault('clipping_enabled', False)
		
	def setClippingEnabled(self, state):
		self.userProps()['clipping_enabled'] = state

	def viewOptions(self):
		viewOptions = {'Camera Visibility': {}, 'Camera Display': {}}

		for parameter in self._nativePointer.Properties('Camera Visibility').Parameters:
			viewOptions['Camera Visibility'][ parameter.ScriptName ] = parameter.Value

		for parameter in self._nativePointer.Properties('Camera Display').Parameters:
			viewOptions['Camera Display'][ parameter.ScriptName ] = parameter.Value

		viewOptions[ 'viewcubeshow' ] = xsi.GetValue('preferences.ViewCube.show')
		return viewOptions

	def setViewOptions(self, viewOptions):
		for prop in viewOptions:
			if prop in [ 'Camera Visibility', 'Camera Display' ]:
				for param in viewOptions[prop]:
					if not param in ['hidlincol', 'wrfrmdpthcuecol']:
						try:
							self._nativePointer.Properties(prop).Parameters(param).Value = viewOptions[prop][param]
						except:
							print 'TRACEBACK: skipping param: {} {}...'.format(prop, param)
							print traceback.format_exc()

		xsi.SetValue('preferences.ViewCube.show', viewOptions.get('viewcubeshow'), xsi.GetValue('preferences.ViewCube.show'))
		return True



	def isVrayCam(self):
		return False


# register the symbol
from blur3d import api
api.registerSymbol('SceneCamera', SoftimageSceneCamera)
