##
#	\namespace	blur3d.api.abstract.abstractscenerenderer
#
#	\remarks	The StudiomaxSceneRenderer class provides an interface to editing renderers in a Scene environment for a Studiomax application
#	
#	\author		eric@blur.com
#	\author		Blur Studio
#	\date		09/08/10
#

from Py3dsMax 										import mxs
from blur3d.api.abstract.abstractscenerenderer 		import AbstractSceneRenderer

class StudiomaxSceneRenderer( AbstractSceneRenderer ):
	#------------------------------------------------------------------------------------------------------------------------
	# 												protected methods
	#------------------------------------------------------------------------------------------------------------------------
	def _nativeProperty( self, key, default = None ):
		"""
			\remarks	implements AbstractSceneRenderer._nativeProperty to return the value of the property defined by the inputed key
			\sa			hasProperty, setProperty, _nativeProperty, AbstractScene._fromNativeValue
			\param		key			<str>
			\param		default		<variant>	(auto-converted from the application's native value)
			\return		<variant>
		"""
		return self._nativePointer.property( str(key) )
		
	def _setNativeProperty( self, key, nativeValue ):
		"""
			\remarks	implements AbstractSceneRenderer._setNativeProperty to set the value of the property defined by the inputed key
			\sa			hasProperty, property, setProperty, AbstractScene._toNativeValue
			\param		key		<str>
			\param		value	<variant>	(pre-converted to the application's native value)
			\retrun		<bool> success
		"""
		self._nativePointer.setProperty( str( key ), nativeValue )
		return True
		
	#------------------------------------------------------------------------------------------------------------------------
	# 												public methods
	#------------------------------------------------------------------------------------------------------------------------
	def edit( self ):
		"""
			\remarks	implements AbstractSceneRenderer.edit to allow the user to edit the renderer
			\return		<bool> success
		"""
		medit = mxs.medit
		medit.PutMtlToMtlEditor( self._nativePointer, medit.GetActiveMtlSlot() )
		mxs.matEditor.open()
		return True
	
	def hasProperty( self, key ):
		"""
			\remarks	implements AbstractSceneRenderer.hasProperty to check to see if the inputed property name exists for this renderer
			\sa			property, setProperty
			\param		key		<str>
			\return		<bool> found
		"""
		return mxs.isProperty( self._nativePointer, str(key) ) or mxs.hasProperty( self._nativePointer, str(key) )
	
	def rendererType( self ):
		"""
			\remarks	implements AbstractSceneRenderer.rendererType to return the renderer type for this instance
			\sa			setRendererType
			\return		<blur3d.constants.RendererType>
		"""
		from blur3d.constants import RendererType
		classname = str(mxs.classof(self._nativePointer)).lower()
		
		if ( classname == 'default_scanline_renderer' ):
			return RendererType.Scanline
		elif ( classname == 'mental_ray_renderer' ):
			return RendererType.MentalRay
		elif ( 'v_ray' in classname ):
			return RendererType.VRay
		
		return 0
		
# register the symbol
from blur3d import api
api.registerSymbol( 'SceneRenderer', StudiomaxSceneRenderer )